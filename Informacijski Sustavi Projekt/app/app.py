from flask import Flask, request, jsonify, render_template, redirect, url_for # type: ignore
from flask_mysqldb import MySQL# type: ignore
import MySQLdb.cursors # type: ignore

# Inicijalizacija Flask aplikacije
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Inicijalizacija MySQL veze
mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM zadaci')
    zadaci = cursor.fetchall()
    return render_template('index.html', zadaci=zadaci)

# Kreiraj zadatak
@app.route('/dodaj', methods=['POST'])
def dodaj_zadatak():
    naslov = request.form['naslov']
    opis = request.form['opis']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO zadaci (naslov, opis) VALUES (%s, %s)', (naslov, opis))
    mysql.connection.commit()
    return redirect(url_for('index'))

# Prikaz zadataka
@app.route('/zadaci', methods=['GET'])
def prikazi_zadatke():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM zadaci')
    zadaci = cursor.fetchall()
    return jsonify(zadaci)

# Ažuriraj zadatak
@app.route('/azuriraj/<int:id>', methods=['POST'])
def azuriraj_zadatak(id):
    naslov = request.form['naslov']
    opis = request.form['opis']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE zadaci SET naslov = %s, opis = %s WHERE id = %s', (naslov, opis, id))
    mysql.connection.commit()
    return redirect(url_for('index'))

# Izbriši zadatak
@app.route('/izbrisi/<int:id>', methods=['POST'])
def izbrisi_zadatak(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM zadaci WHERE id = %s', (id,))
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
