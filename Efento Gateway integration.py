import psycopg2

from flask import Flask, request, Response, json, g

app = Flask(__name__)
# This scripts saves the measurements sent by Efento Gateway in a PostgreSQL database.
# Enter your database credentials: database host, name, user and password
DATABASE_HOST = 'host_name';
DATABASE_USER = 'database_user';
DATABASE_PASSWORD = 'database_password';
DATABASE_NAME = 'database_name';

# Connecting to the database
conn = psycopg2.connect(
    dbname=DATABASE_NAME,
    user=DATABASE_USER,
    host=DATABASE_HOST,
    password=DATABASE_PASSWORD
)
# Set up "/api/v2/measurements" endpoint, which will be receiving the data sent by Efento Gateway using POST method


@app.route('/api/v2/measurements', methods=['POST'])
def respond():
    data = request.json
    record = []
    response_handle = []

    # Use a loop to create record by iterating through measurements and parameters from JSON.
    for measurement in data['measurements']:

        for param in measurement['params']:
            record.extend([(measurement['measured_at'], measurement['serial'], measurement['battery'], param['type'],
                            param['value'])])
        # Create the response body, which will be sent to the gateway (gateway will buffer data from all sensors)
        response_handle.append(measurement['response_handle'])
    response = json.dumps(({'Y': response_handle, 'N': []}))
    # Insert data received from gateway into the database
    measurements = "INSERT INTO measurements(measured_at, serial_number, low_battery, type, value) VALUES (%s, %s, %s, %s, %s)"
    with conn.cursor() as cur:
        try:
            # inserting a list of sensor parameters and measurement to table in PostgresSQL
            cur.executemany(measurements, record)
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return Response(status="500")
    # Send response body, to the gateway and status code 201.
    return Response(response, status='201')

# Start the application on Your port.Default port 5000
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
