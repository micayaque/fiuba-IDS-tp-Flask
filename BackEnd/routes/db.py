import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="mica",
        password="papasfritas",
        database="tpbuddy"
    )