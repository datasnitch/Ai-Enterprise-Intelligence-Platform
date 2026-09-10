from enterprise.database.mysql_connector import connect

conn = connect()

print("Database Connected Successfully!")

conn.close()