from google.cloud.sql.connector import Connector
import mysql.connector
import pandas as pd
from .constants import *
import sys

# we are encoding all to utf-8
if sys.stdout.encoding != 'UTF-8':
    sys.stdout.reconfigure(encoding='UTF-8')


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


def query_df(query, values=None):
    try:
        with getconn() as mydb:
            cursor = mydb.cursor()
            cursor.execute(query, values)
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


def job_data_with_id(id):
    query = "select * From job_data WHERE id = %s"
    data = query_df(query, (id,))
    return data

# query = "select * From job_data"
# # # with open('query.txt') as f:
# # #     new_query = f.read()
# #
# data = query_df(query)
# print(data)
# query_update_table(new_query)


def add_application_db(job_id, data):
    try:
        with getconn() as mydb:
            cursor = mydb.cursor()
            query = ("INSERT INTO applications "
                     "(job_id, full_name, email, phone, linkedin_url, education, work_experience, resume_url, cover_letter) "  # Corrected to include phone and cover_letter
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")  # Nine placeholders

            values = (
                job_id,
                data.get("full_name"),  # Use .get() for safety
                data.get("email_id"),
                data.get("phone"),  # Added phone
                data.get("linkedin_profile"),
                data.get("education"),
                data.get("work_experience"),
                data.get("resume"),
                data.get("cover_letter")  # Added cover_letter
            )
            cursor.execute(query, values)  # Pass values as a tuple
            mydb.commit()
            print("Record updated successfully")
    except mysql.connector.Error as err:
        import logging  # Add logging
        logging.error(f"Error inserting application into database: {err}")
        return None