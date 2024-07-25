from google.cloud.sql.connector import Connector
import mysql.connector
from .constants import *
import pandas as pd

# Initialize Connector object
connector = Connector()


# Function to get a database connection
def getconn() -> mysql.connector.MySQLConnection:
    conn = connector.connect(
        instance_connection_name,
        "pymysql",  # Specify the MySQL dialect
        user=db_user,
        password=db_pass,
        db=db_name
    )
    return conn


# Connect to the database


def query_df(query):
    try:
        with getconn() as mydb:
            cursor = mydb.cursor()
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]  # Get column names
            data = cursor.fetchall()

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=columns)
        return df
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def query_update_table(query):
    try:
        with getconn() as mydb:
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            print("Record updated successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


query = "select * From job_data"
# with open('query.txt') as f:
#     new_query = f.read()

# data = query_df(query)
# print(data)
# query_update_table(new_query)
# data = query_df(query)
# print(data)