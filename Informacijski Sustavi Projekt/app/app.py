from flask import Flask, request, jsonify, render_template, redirect, url_for # type: ignore
from flask_mysqldb import MySQL # type: ignore
import MySQLdb.cursors # type: ignore
from datetime import datetime, timedelta

# Inicijalizacija Flask aplikacije
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Inicijalizacija MySQL veze
mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM clan ORDER BY prezime')
    clanovi = cursor.fetchall()
    return render_template('index.html', clanovi=clanovi)

# Kreiraj clana
@app.route('/dodaj', methods=['POST'])
def dodaj_clana():
    ime = request.form['ime']
    prezime = request.form['prezime']
    preplata = int(request.form['preplata'])
    
    # Calculate the preplata_datum and preplata_istece
    preplata_datum = datetime.now().date()
    preplata_istece = preplata_datum

    if preplata == 1:
        preplata_istece += timedelta(days=30)
    elif preplata == 3:
        preplata_istece += timedelta(days=90)
    elif preplata == 6:
        preplata_istece += timedelta(days=180)
    elif preplata == 12:
        preplata_istece += timedelta(days=365)

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO clan (ime, prezime, preplata, preplata_datum, preplata_istece) VALUES (%s, %s, %s, %s, %s)', 
                       (ime, prezime, True, preplata_datum, preplata_istece))
        mysql.connection.commit()
        fix_ids()
        print("Record inserted successfully")
    except MySQLdb.Error as e:
        print(f"Error inserting data: {e}")
    return redirect(url_for('index'))

# Ažuriraj clana
@app.route('/azuriraj/<int:korisnik_id>', methods=['POST'])
def azuriraj_clana(korisnik_id):
    ime = request.form['ime']
    prezime = request.form['prezime']
    preplata = 'preplata' in request.form  # Checkbox handling
    preplata_datum = request.form['preplata_datum']
    preplata_istece = request.form['preplata_istece']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE clan SET ime = %s, prezime = %s, preplata = %s, preplata_datum = %s, preplata_istece = %s WHERE korisnik_id = %s', 
                   (ime, prezime, preplata, preplata_datum, preplata_istece, korisnik_id))
    mysql.connection.commit()
    return redirect(url_for('index'))

# Izbriši clana
@app.route('/izbrisi/<int:korisnik_id>', methods=['POST'])
def izbrisi_clana(korisnik_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM clan WHERE korisnik_id = %s', (korisnik_id,))
    mysql.connection.commit()
    fix_ids()
    return redirect(url_for('index'))

# Detalji clana
@app.route('/clan/<int:korisnik_id>')
def detalji_clana(korisnik_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM clan WHERE korisnik_id = %s', (korisnik_id,))
    clan = cursor.fetchone()
    return render_template('member.html', clan=clan)

# Fix IDs to be sequential and grouped by last name
def fix_ids():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM clan ORDER BY prezime')
    clanovi = cursor.fetchall()
    for i, clan in enumerate(clanovi, start=1):
        cursor.execute('UPDATE clan SET korisnik_id = %s WHERE korisnik_id = %s', (i, clan['korisnik_id']))
    mysql.connection.commit()

if __name__ == '__main__':
    app.run(debug=True)
