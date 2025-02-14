import os
import pymysql
from flask import jsonify
import json
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text, create_engine, MetaData, Table, Column, Numeric, Integer, VARCHAR, update

# ✅ Hardcoded database credentials (Avoid in production)
db_user = "user1"
db_password = "1234"
db_name = "sql1"
db_connection_name = "projectlaxmi09:us-central1:sql1"


def open_connection():
    """Establish a connection to the Cloud SQL database."""
    connector = Connector()
    
    conn = connector.connect(
        db_connection_name,
        "pymysql",
        user=db_user,
        password=db_password,
        db=db_name
    )
    return conn


def validate_patient(first_name, last_name, password):
    """Fetch all patient records."""
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    with pool.connect() as db_conn:
        results = db_conn.execute(sqlalchemy.text("SELECT * FROM patients")).fetchall()
    db_conn.close()
    return results


def validate_doctor_db(doctor_name, password):
    """Validate doctor credentials."""
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    with pool.connect() as db_conn:
        query = f"SELECT * FROM patients WHERE doctor_name = '{doctor_name}' AND doctor_password = '{password}';"
        results = db_conn.execute(sqlalchemy.text(query)).fetchall()
    db_conn.close()
    return results
