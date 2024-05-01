Alle commando's voor docker compose
1. Je moet in de Folder gaan waar de Dokcer-compose.yml zit
2. Je moet gewoon < docker compose up -d > doen om het op te starten.

Nuttige commando's:
<docker compose down> om het uit te zetten
<docker-compose build [filenaam]> om een file te updaten die je hebt aangepast

Voor de headers aan te passen moet je postman gebruiken.
1. Importeer Inventree Api.yaml in postman.
2. Ga naar authorization en kies in de dropdown voor basic auth.
3. Vul uw super user in als je eer geen hebt  (Probeer iedereen met user: admin passwoord: ehb123)
Anders ga je zelf een moeten aanmaken met <docker compose run --rm inventree-server invoke superuser> 
4. Ga naar headers en copy/past authorization en cookie waar het moet in de code(Cookie staat 2x in code authorization 1x)

Als ik iets heb vergeten vraag het direct!
git rm --cached inventree-data






docker compose up -d
docker compose run --rm inventree-server invoke update

Om een extra admin aan te maken => docker compose run --rm inventree-server invoke superuser

Om container down te doen => docker compose down