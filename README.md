# Dokumentacija za Web Servis za Upravljanje Članovima Teretane

## Use case

![Use Case Diagram](https://github.com/Wulfgar68/Teretana/assets/69584543/e0a5c9e8-afa7-40b7-8f97-fada5282e942)

Ovaj web servis omogućava administratorima teretane upravljanje članovima teretane putem sljedećih funkcionalnosti:
- **Dodavanje člana**: Administrator može dodati novog člana u sustav s osnovnim informacijama kao što su ime, prezime, i trajanje preplate.
- **Ažuriranje člana**: Administrator može ažurirati informacije postojećeg člana, uključujući produženje preplate.
- **Brisanje člana**: Administrator može izbrisati člana iz sustava.
- **Pretraga članova**: Administrator može pretraživati članove prema imenu i prezimenu.
- **Resetiranje ID-eva**: Administrator može resetirati ID-eve članova kako bi bili kontinuirani bez praznina.

**Instalacija**
Skidanje koda s GitHub-a:
```bash
cd ~/Downloads
git clone https://github.com/Wulfgar68/Teretana
cd Teretana
```
Docker tutorial:
```bash
docker build -t teretana .
docker-compose up
docker ps
```
