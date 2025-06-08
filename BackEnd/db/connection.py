# connection.py
import mysql.connector
from BackEnd.config import MYSQL_CONFIG

def get_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)
