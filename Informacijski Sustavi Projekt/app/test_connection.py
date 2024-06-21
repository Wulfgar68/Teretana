import mysql.connector# type: ignore
from mysql.connector import Error # type: ignore

print("Pocetak")

# Inicijalizacija varijable connection
connection = None

# Uspostavljanje veze s bazom podataka
try:
    print("Spajanje na bazu...")
    connection = mysql.connector.connect(
        host='localhost',
        database='Luka PIS',
        user='luka_pis',
        password='luka23012005'
    )
    if connection.is_connected():
        print("Uspjesno spojeno")

except Error as e:
    print("Error prilikom spajanja na MySQL", e)

finally:
    if connection is not None and connection.is_connected():
        connection.close()
        print("MySQL veza je zatvorena")
