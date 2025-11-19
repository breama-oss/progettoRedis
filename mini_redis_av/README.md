📘 Mini Redis AV Server
Python + Flask + Redis + FFmpeg

Mini Redis AV Server è un progetto didattico che combina backend Python, processing multimediale, Redis come database key–value e una UI web semplice in italiano.

Consente di:

📤 Caricare file video

🧪 Estrarre metadata tramite ffprobe

🖼️ Generare thumbnail JPEG tramite ffmpeg

🗄️ Salvare i dati in Redis (reale)

🌐 Esporre API REST

🖥️ Fornire una dashboard HTML minimale

È un esempio completo di:
✔ backend Flask • ✔ Redis • ✔ multimedia processing • ✔ REST API • ✔ UI web

🧰 Requisiti

Assicurati di avere installato:

Componente	Richiesto	Verifica
Python	≥ 3.9	python3 --version
Redis	≥ 7.0	redis-cli ping
FFmpeg	≥ 4.0	ffmpeg -version
pip + venv	sì	pip --version
🚀 Installazione
1️⃣ Clona il progetto
git clone https://github.com/breama-oss/progettoRedis.git
cd progettoRedis

2️⃣ Crea ambiente virtuale

macOS / Linux

python3 -m venv venv
source venv/bin/activate


Windows (PowerShell)

python -m venv venv
.\venv\Scripts\Activate.ps1

3️⃣ Installa le dipendenze Python
pip install -r requirements.txt

4️⃣ Installa Redis
🪟 Windows (consigliato: WSL2)

Redis non è più supportato nativamente per Windows.
Si consiglia l’uso di WSL2 + Ubuntu.

Installazione WSL2

Apri PowerShell come amministratore:

wsl --install


Riavvia Windows se richiesto.

Avvia Ubuntu:

wsl


Installa Redis:

sudo apt update
sudo apt install redis-server


Avvia:

sudo service redis-server start


Test:

redis-cli ping


Dovresti ottenere:

PONG

🍏 macOS (Homebrew)
brew install redis
brew services start redis


Test:

redis-cli ping

🧩 Architettura del progetto
mini_redis_av/
│── http_server.py        # Server Flask con API e UI
│── av_processor.py       # ffprobe + ffmpeg + Base64 thumb
│── database.py           # Wrapper per Redis
│── templates/
│     ├── index.html      # Lista video
│     ├── upload.html     # Form upload
│     └── video_view.html # Dettaglio video
│── uploads/              # File video caricati

▶️ Avvio del Server

Assicurati che Redis sia attivo, poi:

macOS / Linux

source venv/bin/activate
cd mini_redis_av
python3 http_server.py


Windows PowerShell

.\venv\Scripts\Activate.ps1
cd mini_redis_av
python.exe http_server.py


Server attivo su:

➡️ http://127.0.0.1:5000

🌐 Interfaccia Web
🏠 Homepage
http://localhost:5000/


Mostra:

elenco video caricati

thumbnail

metadata

pulsante elimina

📤 Upload tramite web UI
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
curl http://localhost:5000/videos

3️⃣ Metadati JSON formattati
curl http://localhost:5000/meta/<video_id>

4️⃣ Thumbnail JPEG
curl http://localhost:5000/video/<uuid>/thumb -o thumb.jpg

5️⃣ Eliminare un video
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
video:<uuid>:thumb	Thumbnail Base64
video:<uuid>:path	Percorso file locale
🧪 Test Manuale Completo

Avvia Flask

Carica un video via curl

Apri http://localhost:5000/

Verifica thumbnail e metadata

Controlla Redis:

redis-cli
> KEYS video:*
> GET video:<uuid>

📜 Licenza

MIT — libero uso per studio e sviluppo.