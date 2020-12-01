import mysql.connector

from flask import g


def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="192.168.178.55",
            user="root",
            passwd="Admin!123",
            database="mydb"
        )

    return g.db
