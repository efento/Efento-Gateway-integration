# Efento-Gateway-integration
http server with a database.

**This tutorial will show you how to setup a simple http server with a database and configure Efento gateway to send the data to it. In this tutorial we are using Python, Flask and PostgreSQL database, but the same idea can be easily implemented in other programming languages / with different databases. Should you have any issues or questions, feel free to drop us a line at help.efento.io**

# Before you start

Before you start you will need to install and configure the following components: 


-   [PyCharm](https://www.jetbrains.com/pycharm/download/) or any Python 3 IDE,
-   [PostgreSQL database](https://www.postgresql.org/),
-   [Efento Gateway](https://getefento.com/product/efento-gateway-bluetooth-ethernet/) and [Efento sensors](https://getefento.com/technology/efento-bluetooth-low-energy-wireless-sensors/)

# PostgreSQL database 

## Setting up the database

After downloading and installing PostgreSQL you will need to create the first database. This in one of the steps during the PostgreSQL installation. By default, the database will be created with the following credentials:

_DATABASE_HOST = ‘localhost’;_  
_DATABASE_USER = ‘postgres’;_  
_DATABASE_PASSWORD = ‘Your password’;_  
_DATABASE_NAME = ‘postgres’;_

If you want to, you can change the names / credentials. Write them down, as they will be needed in the next steps. If you want to check database credentials, open pgAdmin in the PostgreSQL folder. **Next open Object -> Properties -> General**

![](https://getefento.com/wp-content/uploads/2021/05/Database-credentials.png)

## Creating a table

To save the measurements coming from Efento Gateway in your database, you need to create a table. In this example, we are creating a very simple table to store all the data from the sensors, no matter what the sensor type. The table will have 5 columns, all of them of “text” type. **Please note that this architecture of the database is only for the demonstration purposes. Database structure should be selected according to your project requirements.**  

You can create the table manually, using pgAdmin’s interface or using a SQL query. In pgAdmin select your database, open Tools menu: **Tools -> Query Tools**. Copy the request below into the **Query Editor** and click **Execute** (▶) :


    CREATE  TABLE measurements (
        measured_at text ,
        serial_number text ,
        low_battery text ,
        type text,
        value text);

![](https://getefento.com/wp-content/uploads/2021/05/Create-table.png)

# Python Server

## **Before you start**

In order to make the server work, you will need:

-   **Flask** – Flask is a micro framework used for development of web applications. If you want to learn more about Flask check out [this website](https://flask.palletsprojects.com/en/2.0.x/). You can install and import Flask in pyCharm IDE or using pip ($ pip install -U Flask)
-   **psycopg2** – one of the most popular PostgreSQL database adapter for Python. If You want to know more check out [this website](https://www.psycopg.org/docs/).

### **How it works?**

Script we are going to write sets up http server. The server is constantly listening for data sent by Efento Gateway (gateway sends the data as JSON over REST. One message can contain multiple measurements from one sensor or measurements from multiple sensors. Once a new messages comes, server parses the data, saves it in the data base and returns “201” status code to the gateway. This means that the message has been successfully parsed and save in the database. If anything goes wrong (e.g. database is down), server will respond with “500” status code to gateway. In that case, gateway will retry to send the same data after a while.

![](https://getefento.com/wp-content/uploads/2021/05/Server-algorithm.png)

## **Efento gateway configuration**

Log in to Efento Gateway’s web panel through your web browser. Navigate to **Settings** -> **Server settings**.

![](https://getefento.com/wp-content/uploads/2021/05/Gateway-settings1.png)

In the **Connection To Server** field select **Custom Settings**. Fill in the server address (either domain or IP of the computer / server which runs the Python script) in the **Server Address** field. Configure the **Server port** to **5000** and switch **TLS** off. Note! If TLS is switched off, the data sent by the gateway is not encrypted. For production deployments, you should upload your server’s certificate in the **CA certificate** tab and use encrypted communication (htpps).

![](https://getefento.com/wp-content/uploads/2021/05/Gateway-settings2.png)

## **Results**

When you run the script, all the data coming form the gateway will be saved in the database. To view the measurements open pgAdmin 4, select your database, then open **Tools** > **Query Tools**.

Enter the request below into the **Query Editor** and select **Execute** (▶) :

> **SELECT**  * **FROM** measurements;

![](https://getefento.com/wp-content/uploads/2021/05/Display-table.png)
