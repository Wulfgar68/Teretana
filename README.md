# Dokumentacija za Web Servis za Upravljanje Članovima Teretane

## Use case

![Use Case Diagram](Teretana PIS.png)

Ovaj web servis omogućava administratorima teretane upravljanje članovima teretane putem sljedećih funkcionalnosti:
- **Dodavanje člana**: Administrator može dodati novog člana u sustav s osnovnim informacijama kao što su ime, prezime, i trajanje preplate.
- **Ažuriranje člana**: Administrator može ažurirati informacije postojećeg člana, uključujući produženje preplate.
- **Brisanje člana**: Administrator može izbrisati člana iz sustava.
- **Pretraga članova**: Administrator može pretraživati članove prema imenu i prezimenu.
- **Resetiranje ID-eva**: Administrator može resetirati ID-eve članova kako bi bili kontinuirani bez praznina.

## Pokretanje web servisa s Docker-om

1. **Preduvjeti**:
    - Instaliran Docker i Docker Compose.

2. **Pokretanje servisa**:
    - U terminalu, navigirajte do direktorija projekta.
    - Pokrenite Docker kontejnere s naredbom:
      ```bash
      docker-compose up
      ```

3. **Pristup servisu**:
    - Nakon što su kontejneri pokrenuti, servis će biti dostupan na `http://localhost:5000`.

## Prolazak kroz funkcionalnosti web servisa

1. **Dodavanje člana**:
    - Na početnoj stranici, kliknite na gumb "Dodaj Člana".
    - Ispunite formu s imenom, prezimenom i trajanjem preplate.
    - Kliknite na gumb "Dodaj Člana" kako biste dodali novog člana.

2. **Ažuriranje člana**:
    - Na početnoj stranici, kliknite na gumb "Upravljaj Članovima".
    - Kliknite na gumb "Ažuriraj" pored člana kojeg želite ažurirati.
    - Ažurirajte informacije u formi i kliknite na gumb "Ažuriraj" kako biste spremili promjene.

3. **Brisanje člana**:
    - Na početnoj stranici, kliknite na gumb "Upravljaj Članovima".
    - Kliknite na gumb "Obriši" pored člana kojeg želite izbrisati.
    - Član će biti uklonjen iz sustava.

4. **Pretraga članova**:
    - Na početnoj stranici, unesite ime i/ili prezime člana kojeg tražite u odgovarajuća polja za pretragu.
    - Kliknite na gumb "Pretraži" kako biste filtrirali članove prema unesenim kriterijima.

5. **Resetiranje ID-eva**:
    - Na stranici za upravljanje članovima, kliknite na gumb "Resetiraj ID-ove".
    - ID-evi članova će biti resetirani i kontinuirani bez praznina.

Ovaj web servis omogućuje učinkovito upravljanje članovima teretane i olakšava administrativne zadatke.
