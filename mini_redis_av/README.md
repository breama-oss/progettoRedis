📘 README.md — Mini Redis AV Server (Python + Flask + Redis + FFmpeg)
🎯 Descrizione del progetto

Mini Redis AV Server è un progetto didattico che replica una parte del funzionamento di Redis, aggiungendo funzionalità multimediali:

Upload di file video

Estrazione metadata video tramite ffprobe

Generazione di thumbnail tramite ffmpeg

Salvataggio metadati e preview in Redis reale

API REST

Interfaccia Web in italiano

È un esempio completo di:

backend Python

database key–value Redis

elaborazione audio/video

API HTTP

mini dashboard HTML

🧰 Requisiti

Assicurati di avere installato:

Componente	Richiesto	Verifica
Python	≥ 3.9	python3 --version
Redis	≥ 7.0	redis-cli ping
FFmpeg	≥ 4.0	ffmpeg -version
Pip + venv	sì	pip --version

🚀 Installazione
1. Clona il progetto
git clone https://github.com/breama-oss/progettoRedis.git
cd progettoRedis

2. Crea ambiente virtuale
python3 -m venv venv
source venv/bin/activate

3. Installa le dipendenze Python
pip install -r requirements.txt


4. Installa Redis

Windows

Redis raccomanda l’uso di WSL2 (Windows Subsystem for Linux).

- Installa WSL2

Apri PowerShell come amministratore:

wsl --install


Riavvia Windows quando richiesto.

- Avvia Ubuntu da Start oppure:
wsl

- Installa Redis all’interno di Ubuntu:
sudo apt update
sudo apt install redis-server

- Avvia Redis:
sudo service redis-server start

- Test:
redis-cli ping


Dovresti ottenere:

PONG


macOS (Homebrew)
brew install redis
brew services start redis

Controllo
redis-cli ping


Risultato:

PONG

🧩 Architettura del progetto
mini_redis_av/
│── http_server.py        # Server Flask con API e UI
│── av_processor.py       # ffprobe + ffmpeg + encode Base64
│── database.py           # Wrapper Redis
│── templates/
│     ├── index.html      # Lista video
│     ├── upload.html     # Upload form
│     └── video_view.html # Pagina dettaglio
│── uploads/              # Cartella file video caricati

▶️ Avvio del Server

Assicurati che Redis sia in esecuzione, poi:

.\venv\Scripts\Activate.ps1 (Windows Powershell)
source venv/bin/activate (macOS / Git Bash)
cd mini_redis_av
python3 http_server.py


Server attivo su:

http://127.0.0.1:5000

🌐 Interfaccia Web

Vai in browser su:

Homepage
http://localhost:5000/


Mostra:

elenco video caricati

anteprima thumbnail

link ai metadata

pulsante Elimina

Upload Web
http://localhost:5000/upload_form

📡 API REST
1️⃣ Caricare un video 
curl -F "file=@/percorso/video.mp4" http://localhost:5000/upload_form


Risposta:

{
  "key": "video:<uuid>",
  "meta": { ... }
}

2️⃣ Lista di tutti i video
GET /videos


Esempio:

curl http://localhost:5000/videos

3️⃣ Metadati JSON formattati
GET /meta/<video_id>


Esempio:

curl http://localhost:5000/meta/82b301e2-0035-4c43-84dd-df7e347d1982

4️⃣ Thumbnail JPEG
GET /video/<id>/thumb


Esempio:

curl http://localhost:5000/video/<uuid>/thumb -o thumb.jpg

5️⃣ Eliminare un video e relative chiavi Redis
DELETE /video/<id>


Esempio:

curl -X DELETE http://localhost:5000/video/<uuid>


Risposta:

{
  "deleted_keys": 3,
  "video_id": "<uuid>"
}

🗄️ Struttura delle chiavi Redis

Ogni video genera:

Chiave	Contenuto
video:<uuid>	Metadata JSON
video:<uuid>:thumb	Thumbnail base64
video:<uuid>:path	Percorso file locale

🧪 Test manuale completo

Avvia Flask

Carica un video via curl

Vai su http://localhost:5000/ e verifica

Guarda i metadata

Guarda la thumbnail

Controlla Redis:

redis-cli
> KEYS video:*
> GET video:<uuid>
