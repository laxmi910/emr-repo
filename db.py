#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 11:18:17 2023

@author: dutami
"""

#db.py
import os
import pymysql
from flask import jsonify
import json
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy import text, create_engine, MetaData,\
Table, Column, Numeric, Integer, VARCHAR, update

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    # initialize Connector object
    connector = Connector()
    
    # function to return the database connection object
    conn = connector.connect(
            db_connection_name,
            "pymysql",
            user=db_user,
            password=db_password,
            db=db_name
        )
    return conn


def validate_patient(first_name, last_name, password):
    # create connection pool with 'creator' argument to our connection object function
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    # connect to connection pool
    with pool.connect() as db_conn:
      results = db_conn.execute(sqlalchemy.text("SELECT * FROM patients")).fetchall()
    db_conn.close()
    return results

def validate_doctor_db(doctor_name, password):
    # create connection pool with 'creator' argument to our connection object function
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    # connect to connection pool
    with pool.connect() as db_conn:
      query = "SELECT * FROM patients where doctor_name =\'"+doctor_name+"\'"+" and doctor_password=\'"+password+"\';"
      results = db_conn.execute(sqlalchemy.text(query)).fetchall()
    db_conn.close()
    return results

def validate_insurance_db(insurance_provider):
    # create connection pool with 'creator' argument to our connection object function
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    # connect to connection pool
    with pool.connect() as db_conn:
      query = "SELECT * FROM patients where insurance_provider =\'"+insurance_provider+"\';"
      results = db_conn.execute(sqlalchemy.text(query)).fetchall()
    db_conn.close()
    return results

def validate_hospital_db(hospital_name):
    # create connection pool with 'creator' argument to our connection object function
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    # connect to connection pool
    with pool.connect() as db_conn:
      query = "SELECT * FROM patients where hospital_name =\'"+hospital_name+"\';"
      results = db_conn.execute(sqlalchemy.text(query)).fetchall()
    db_conn.close()
    return results

def view_patient_history_db(doctor_name, first_name, last_name):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    # connect to connection pool
    with pool.connect() as db_conn:
      query = "SELECT * FROM patients where doctor_name =\'"+doctor_name+"\'"+" and first_name=\'"+first_name+"\'" + " and last_name=\'"+last_name+"\';"
      results = db_conn.execute(sqlalchemy.text(query)).fetchall()
    db_conn.close()
    return results

def get_medical_record_db(patient_id):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    # connect to connection pool
    with pool.connect() as db_conn:
      query = "SELECT * FROM patients where patient_id=\'"+patient_id+"\';"
      results = db_conn.execute(sqlalchemy.text(query)).fetchall()
    db_conn.close()
    return results

def update_medical_record_db_old(patient_id,first_name,last_name,dob,sex,blood_type,height,weight,allergies,medications,medical_conditions,heart_rate,blood_pressure):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    new_height = height.replace("'", "\\'")
    new_height = new_height.replace('"', '\\"')
    # connect to connection pool
    with pool.connect() as db_conn:
      query = "UPDATE patients SET first_name=\'"+first_name+"\', " \
              +"last_name=\'"+last_name+"\', " \
              +"dob=\'"+dob+"\', " \
              +"sex=\'"+sex+"\', " \
              +"blood_type=\'"+blood_type+"\', " \
              +"height=\'"+new_height+"\', " \
              +"weight=\'"+weight+"\', " \
              +"allergies=\'"+allergies+"\', " \
              +"medications=\'"+medications+"\', " \
              +"medical_conditions=\'"+medical_conditions+"\', " \
              +"heart_rate=\'"+heart_rate+"\', " \
              +"blood_pressure=\'"+blood_pressure+"\'" \
              +" where patient_id=\'"+patient_id+"\';"
      result = db_conn.execute(sqlalchemy.text(query))
      return result
    db_conn.close()
    return "failed" 

def update_medical_record_db(patient_id,first_name,last_name,dob,sex,blood_type,height,weight,allergies,medications,medical_conditions,heart_rate,blood_pressure):
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    # initialize the Metadata Object
    meta = MetaData(bind=engine)
    MetaData.reflect(meta)
    
    
    patients = meta.tables['patients']
 
    # update
    u = update(patients)
    u = u.values({"first_name": first_name})
    u = u.values({"last_name": last_name})
    u = u.values({"dob": dob})
    u = u.values({"sex": sex})
    u = u.values({"blood_type": blood_type})
    u = u.values({"height": height})
    u = u.values({"weight": weight})
    u = u.values({"allergies": allergies})
    u = u.values({"medications": medications})
    u = u.values({"medical_conditions": medical_conditions})
    u = u.values({"heart_rate": heart_rate})
    u = u.values({"blood_pressure": blood_pressure})
    u = u.where(patients.c.patient_id == patient_id)
    engine.execute(u)
     
    # write the SQL query inside the text()
    # block to fetch all records
    sql = text("SELECT * FROM patients where patient_id=\'"+patient_id+"\';")
 
    # Fetch all the records
    result = engine.execute(sql).fetchall()
 
    return result


def get_payment_record_db(patient_id):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    # connect to connection pool
    with pool.connect() as db_conn:
      query = "SELECT * FROM patients where patient_id=\'"+patient_id+"\';"
      results = db_conn.execute(sqlalchemy.text(query)).fetchall()
    db_conn.close()
    return results


def update_payment_record_db_old(patient_id,first_name,last_name,doctor_name,doctor_phone,hospital_name,hospital_phone,insurance_provider,insurance_id):
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    # connect to connection pool
    with pool.connect() as db_conn:
      query = "UPDATE patients SET first_name=\'"+first_name+"\', " \
              +"last_name=\'"+last_name+"\', " \
              +"doctor_name=\'"+doctor_name+"\', " \
              +"doctor_phone=\'"+doctor_phone+"\', " \
              +"hospital_name=\'"+hospital_name+"\', " \
              +"hospital_phone=\'"+hospital_phone+"\', " \
	      +"insurance_provider=\'"+insurance_provider+"\', " \
              +"insurance_id=\'"+insurance_id+"\', " \
              +" where patient_id=\'"+patient_id+"\';"
      result = db_conn.execute(sqlalchemy.text(query))
      return result
    db_conn.close()
    return "failed" 


def update_payment_record_db(patient_id,first_name,last_name,doctor_name,doctor_phone,hospital_name,hospital_phone,insurance_provider,insurance_id):
    engine = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=open_connection,
    )
    # initialize the Metadata Object
    meta = MetaData(bind=engine)
    MetaData.reflect(meta)
    
    
    patients = meta.tables['patients']
 
    # update
    u = update(patients)
    u = u.values({"first_name": first_name})
    u = u.values({"last_name": last_name})
    u = u.values({"doctor_name": doctor_name})
    u = u.values({"doctor_phone": doctor_phone})
    u = u.values({"hospital_name": hospital_name})
    u = u.values({"hospital_phone": hospital_phone})
    u = u.values({"insurance_provider": insurance_provider})
    u = u.values({"insurance_id": insurance_id})
    u = u.where(patients.c.patient_id == patient_id)
    engine.execute(u)
     
    # write the SQL query inside the text()
    # block to fetch all records
    sql = text("SELECT * FROM patients where patient_id=\'"+patient_id+"\';")
 
    # Fetch all the records
    result = engine.execute(sql).fetchall()
    return result
    
    

