import mysql.connector


def connect():

    conn = mysql.connector.connect(

        host="localhost",

        user="root",

        password="Sharau@09",

        database="EnterpriseDB"

    )

    return conn