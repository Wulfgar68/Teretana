CREATE DATABASE IF NOT EXISTS luka_pis;
USE luka_pis;

CREATE TABLE clan (
    korisnik_id INT AUTO_INCREMENT PRIMARY KEY,
    ime VARCHAR(25) NOT NULL,
    prezime VARCHAR(25) NOT NULL,
    preplata BOOL NOT NULL,
    preplata_datum DATE NOT NULL,
    preplata_istece DATE NOT NULL
);