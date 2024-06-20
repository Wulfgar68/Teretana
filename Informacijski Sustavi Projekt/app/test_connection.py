import mysql.connector
from mysql.connector import Error

try:
    print("Connecting to MySQL database...")
    connection = mysql.connector.connect(
        host='localhost',
        database='Luka PIS',
        user='luka_pis',
        password='luka23012005'
    )
    if connection.is_connected():
        print("Connection to MySQL database was successful")

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
