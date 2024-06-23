from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import logging

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

@app.route('/', methods=['GET'])
def index():
    search_name = request.args.get('search_name', '')
    search_lastname = request.args.get('search_lastname', '')
    
    query = Clan.query
    if search_name:
        query = query.filter(Clan.ime.like(f'%{search_name}%'))
    if search_lastname:
        query = query.filter(Clan.prezime.like(f'%{search_lastname}%'))
    
    clanovi = query.all()
    return render_template('index.html', clanovi=clanovi)

@app.route('/dodaj_clana', methods=['GET', 'POST'])
def dodaj_clana():
    if request.method == 'POST':
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
    
    return render_template('dodaj_clana.html')

@app.route('/upravljaj_clanovima')
def upravljaj_clanovima():
    clanovi = Clan.query.all()
    return render_template('upravljaj_clanovima.html', clanovi=clanovi)

@app.route('/update_clana/<int:korisnik_id>', methods=['GET', 'POST'])
def update_clana(korisnik_id):
    clan = Clan.query.get_or_404(korisnik_id)
    if request.method == 'POST':
        ime = request.form['ime']
        prezime = request.form['prezime']
        preplata_datum = datetime.strptime(request.form['preplata_datum'], '%Y-%m-%d').date()
        preplata_istece = datetime.strptime(request.form['preplata_istece'], '%Y-%m-%d').date()
        
        if preplata_istece < preplata_datum:
            flash("Subscription end date cannot be before the start date.")
            return redirect(url_for('update_clana', korisnik_id=korisnik_id))
        
        clan.ime = ime
        clan.prezime = prezime
        clan.preplata_datum = preplata_datum
        clan.preplata_istece = preplata_istece
        
        preplata_duration = request.form['preplata_duration']
        if preplata_duration:
            clan.preplata_istece += timedelta(days=30 * int(preplata_duration))
        
        db.session.commit()
        flash('Clan uspjesno azuriran!')
        return redirect(url_for('upravljaj_clanovima'))
    
    return render_template('update_clana.html', clan=clan)

@app.route('/delete_clana/<int:korisnik_id>', methods=['POST'])
def delete_clana(korisnik_id):
    clan = Clan.query.get_or_404(korisnik_id)
    db.session.delete(clan)
    db.session.commit()
    flash('Clan uspjesno obrisan!')
    return redirect(url_for('upravljaj_clanovima'))

@app.route('/reset_ids', methods=['POST'])
def reset_ids():
    session = db.session()
    session.execute('SET @count = 0')
    session.execute('UPDATE clan SET korisnik_id = @count := @count + 1')
    session.execute('ALTER TABLE clan AUTO_INCREMENT = 1')
    session.commit()
    flash('ID-ovi uspjesno resetovani!')
    return redirect(url_for('upravljaj_clanovima'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
