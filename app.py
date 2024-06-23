from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import logging
import traceback
import sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://luka_pis:luka23012005@db:3306/luka_pis'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class Clan(db.Model):
    korisnik_id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(25), nullable=False)
    prezime = db.Column(db.String(25), nullable=False)
    preplata = db.Column(db.Boolean, nullable=False)
    preplata_datum = db.Column(db.Date, nullable=False)
    preplata_istece = db.Column(db.Date, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    try:
        clanovi = Clan.query.all()
        return render_template('index.html', clanovi=clanovi)
    except Exception as e:
        logging.error("Error occurred while fetching members: %s", e)
        return f"Internal Server Error: {traceback.format_exc()}", 500

@app.route('/dodaj_clana', methods=['GET', 'POST'])
def dodaj_clana():
    if request.method == 'POST':
        try:
            ime = request.form['ime']
            prezime = request.form['prezime']
            preplata_duration = int(request.form['preplata_duration'])
            preplata = True
            preplata_datum = datetime.now().date()
            preplata_istece = preplata_datum + timedelta(days=30 * preplata_duration)
            new_clan = Clan(ime=ime, prezime=prezime, preplata=preplata, preplata_datum=preplata_datum, preplata_istece=preplata_istece)
            db.session.add(new_clan)
            db.session.commit()
            flash('Clan uspjesno dodan!')
            return redirect(url_for('index'))
        except Exception as e:
            logging.error("Error occurred while adding a new member: %s", e)
            return f"Internal Server Error: {traceback.format_exc()}", 500
    return render_template('dodaj_clana.html')

@app.route('/upravljaj_clanovima')
def upravljaj_clanovima():
    try:
        clanovi = Clan.query.all()
        return render_template('upravljaj_clanovima.html', clanovi=clanovi)
    except Exception as e:
        logging.error("Error occurred while fetching members for management: %s", e)
        return f"Internal Server Error: {traceback.format_exc()}", 500

@app.route('/update_clana/<int:korisnik_id>', methods=['GET', 'POST'])
def update_clana(korisnik_id):
    try:
        clan = Clan.query.get_or_404(korisnik_id)
        if request.method == 'POST':
            try:
                clan.ime = request.form['ime']
                clan.prezime = request.form['prezime']
                if 'extend_duration' in request.form and int(request.form['extend_duration']) > 0:
                    extend_duration = int(request.form['extend_duration'])
                    clan.preplata_istece = clan.preplata_istece + timedelta(days=30 * extend_duration)
                else:
                    clan.preplata_datum = datetime.strptime(request.form['preplata_datum'], '%Y-%m-%d').date()
                    clan.preplata_istece = datetime.strptime(request.form['preplata_istece'], '%Y-%m-%d').date()
                db.session.commit()
                flash('Clan uspjesno azuriran!')
                return redirect(url_for('upravljaj_clanovima'))
            except Exception as e:
                logging.error("Error in updating member: %s", e)
                return f"Internal Server Error: {traceback.format_exc()}", 500
        return render_template('update_clana.html', clan=clan, timedelta=timedelta)
    except Exception as e:
        logging.error("Error in update_clana route: %s", e)
        return f"Internal Server Error: {traceback.format_exc()}", 500

@app.route('/delete_clana/<int:korisnik_id>', methods=['POST'])
def delete_clana(korisnik_id):
    try:
        clan = Clan.query.get_or_404(korisnik_id)
        db.session.delete(clan)
        db.session.commit()
        flash('Clan uspjesno obrisan!')
        return redirect(url_for('upravljaj_clanovima'))
    except Exception as e:
        logging.error("Error occurred while deleting the member: %s", e)
        return f"Internal Server Error: {traceback.format_exc()}", 500

@app.route('/reset_ids', methods=['POST'])
def reset_ids():
    try:
        session = sqlalchemy.orm.Session(bind=db.engine)
        connection = session.connection()
        connection.execute('SET @count = 0')
        connection.execute('UPDATE clan SET korisnik_id = @count := @count + 1')
        connection.execute('ALTER TABLE clan AUTO_INCREMENT = 1')
        session.commit()
        flash('ID-ovi uspjesno resetovani!')
        return redirect(url_for('upravljaj_clanovima'))
    except Exception as e:
        logging.error("Error occurred while resetting IDs: %s", e)
        return f"Internal Server Error: {traceback.format_exc()}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
