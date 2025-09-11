#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"


def connect_db():
    """Connect to MySQL server (without specifying a database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",      # adjust if needed
            password="root"   # adjust if needed
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
    except Error as e:
        print(f"Error while creating database: {e}")


def connect_to_prodev():
    """Connect directly to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",      # adjust if needed
            password="root",  # adjust if needed
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to {DB_NAME}: {e}")
    return None


def create_table(connection):
    """Create user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error while creating table: {e}")


def insert_data(connection, csv_file):
    """Insert rows from CSV file if not already present."""
    try:
        cursor = connection.cursor()
        with open(csv_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE email=%s", (email,))
                if not cursor.fetchone():
                    cursor.execute(
                        f"INSERT INTO {TABLE_NAME} (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )
        connection.commit()
    except Error as e:
        print(f"Error while inserting data: {e}")


def stream_rows(connection):
    """Generator to fetch rows one by one from user_data table."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {TABLE_NAME}")
    for row in cursor:
        yield row
    cursor.close()
