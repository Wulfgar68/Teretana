from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, get_flashed_messages # type: ignore
from flask_mysqldb import MySQL # type: ignore
import MySQLdb.cursors # type: ignore
from datetime import datetime, timedelta

# Inicijalizacija Flask aplikacije
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config.from_pyfile('config.py')

# Inicijalizacija MySQL veze
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dodaj_clana', methods=['GET', 'POST'])
def dodaj_clana():
    if request.method == 'POST':
        ime = request.form['ime']
        prezime = request.form['prezime']
        preplata = int(request.form['preplata'])

        # Izračunaj preplata_datum i preplata_istece
        preplata_datum = datetime.now().date()
        preplata_istece = preplata_datum + timedelta(days=30*preplata)

        try:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO clan (ime, prezime, preplata, preplata_datum, preplata_istece) VALUES (%s, %s, %s, %s, %s)', 
                           (ime, prezime, True, preplata_datum, preplata_istece))
            mysql.connection.commit()
            flash('Član je uspješno dodan!', 'success')
        except MySQLdb.Error as e:
            flash(f'Greška prilikom dodavanja člana: {e}', 'danger')
        finally:
            cursor.close()
        return redirect(url_for('dodaj_clana'))

    return render_template('dodaj_clana.html')

@app.route('/upravljaj_clanovima', methods=['GET', 'POST'])
def upravljaj_clanovima():
    poruka = ""
    query = request.args.get('query')
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if query:
            cursor.execute('SELECT * FROM clan WHERE prezime LIKE %s', ('%' + query + '%',))
        else:
            cursor.execute('SELECT * FROM clan')
        clanovi = cursor.fetchall()
    except Exception as e:
        print("Greška prilikom preuzimanja članova iz baze: ", e)
        clanovi = []
    finally:
        if 'cursor' in locals():
            cursor.close()
    return render_template('upravljaj_clanovima.html', clanovi=clanovi, query=query, poruka=poruka)

@app.route('/azuriraj/<int:korisnik_id>', methods=['POST'])
def azuriraj_clana(korisnik_id):
    ime = request.form['ime']
    prezime = request.form['prezime']
    preplata = 'preplata' in request.form
    preplata_datum = request.form['preplata_datum']
    preplata_istece = request.form['preplata_istece']
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE clan SET ime = %s, prezime = %s, preplata = %s, preplata_datum = %s, preplata_istece = %s WHERE korisnik_id = %s', 
                       (ime, prezime, preplata, preplata_datum, preplata_istece, korisnik_id))
        mysql.connection.commit()
        flash('Član je uspješno ažuriran!', 'success')
    except MySQLdb.Error as e:
        flash(f'Greška prilikom ažuriranja člana: {e}', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('upravljaj_clanovima'))

@app.route('/izbrisi/<int:korisnik_id>', methods=['POST'])
def izbrisi_clana(korisnik_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM clan WHERE korisnik_id = %s', (korisnik_id,))
        mysql.connection.commit()
        flash('Član je uspješno izbrisan!', 'success')
    except MySQLdb.Error as e:
        flash(f'Greška prilikom brisanja člana: {e}', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('upravljaj_clanovima'))

@app.route('/fix_ids', methods=['POST'])
def fix_ids():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SET @count = 0')
        cursor.execute('UPDATE clan SET korisnik_id = @count:= @count + 1 ORDER BY prezime, ime')
        cursor.execute('ALTER TABLE clan AUTO_INCREMENT = 1')
        mysql.connection.commit()
        flash('ID-ovi članova su uspješno popravljeni!', 'success')
    except MySQLdb.Error as e:
        flash(f'Greška prilikom popravljanja ID-ova: {e}', 'danger')
    finally:
        cursor.close()
    return redirect(url_for('upravljaj_clanovima'))

if __name__ == '__main__':
    app.run(debug=True)
