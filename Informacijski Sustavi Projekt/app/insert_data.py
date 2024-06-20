import pandas as pd
import mysql.connector
from mysql.connector import Error

print("Početak")

# Put do vašeg CSV fajla
csv_file_path = 'T:\\Informacijski Sustavi Projekt\\app\\clanovi.csv'

# Čitanje CSV fajla
try:
    print("Čitanje...")
    df = pd.read_csv(csv_file_path)
    print("Pročitano, podaci:")
    print(df)
except Exception as e:
    print(f"ERROR čitanje: {e}")

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
        print("Uspješno spojeno")
        cursor = connection.cursor()

        # Ubacivanje zapisa iz DataFrame-a jedan po jedan
        print("Ubacivanje podataka u bazu...")
        for i, row in df.iterrows():
            try:
                sql = """INSERT INTO clan (prezime, preplata, vrijeme_u_prostoru, preplata_datum, preplata_istece)
                         VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, tuple(row[1:]))  # Preskakanje prvog stupca (korisnik_id) jer je auto-increment
            except Error as e:
                print(f"ERROR ubacivanja redaka {i}: {e}")

        # Potvrđivanje transakcije
        try:
            connection.commit()
            print("Zapisi uspješno ubačeni")
        except Error as e:
            print(f"Error potvrđivanja transakcije: {e}")

except Error as e:
    print("Error prilikom spajanja na MySQL ili ubacivanja podataka", e)

finally:
    if connection is not None and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL veza je zatvorena")
