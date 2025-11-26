Mini Redis AV Server

Descrizione generale

Mini Redis AV Server è un progetto didattico che permette di caricare file video, analizzarli tramite FFmpeg/ffprobe, generare thumbnail, salvare i metadati in Redis ed esporre un’interfaccia web e API REST tramite Flask.

Funzionalità principali

Caricamento file video

Estrazione metadata tramite ffprobe

Generazione thumbnail JPEG via ffmpeg

Salvataggio dati in Redis

API REST

Dashboard HTML minimale

Requisiti
Componente	Versione minima	Verifica
Python	≥ 3.9	python3 --version
Redis	≥ 7.0	redis-cli ping
FFmpeg	≥ 4.0	ffmpeg -version
pip + venv	sì	pip --version
Installazione
1. Clona il progetto
git clone https://github.com/breama-oss/progettoRedis.git
cd progettoRedis

2. Crea l’ambiente virtuale

macOS / Linux

python3 -m venv venv
source venv/bin/activate


Windows (PowerShell)

python -m venv venv
.\venv\Scripts\Activate.ps1

3. Installa le dipendenze Python
pip install -r requirements.txt

4. Installa Redis
Windows (consigliato WSL2)

Redis non è supportato nativamente su Windows.

wsl --install
wsl
sudo apt update
sudo apt install redis-server
sudo service redis-server start
redis-cli ping


Output atteso:

PONG

macOS (Homebrew)
brew install redis
brew services start redis
redis-cli ping

Architettura del progetto
mini_redis_av/
├── http_server.py        # Server Flask (API + UI)
├── av_processor.py       # ffprobe, ffmpeg, thumbnail Base64
├── database.py           # Wrapper per Redis
├── templates/
│   ├── index.html
│   ├── upload.html
│   └── video_view.html
└── uploads/

Avvio del server

macOS / Linux

source venv/bin/activate
cd mini_redis_av
python3 http_server.py


Windows PowerShell

.\venv\Scripts\Activate.ps1
cd mini_redis_av
python.exe http_server.py


Server attivo:

http://127.0.0.1:5000

Interfaccia Web

Homepage
http://localhost:5000/

Mostra:

elenco video caricati

thumbnail

metadata

pulsante elimina

Upload Web
http://localhost:5000/upload_form

API REST
1. Caricare un video
curl -F "file=@/percorso/video.mp4" http://localhost:5000/upload_form


Risposta:

{
  "key": "video:<id>",
  "meta": { }
}

2. Lista dei video
curl http://localhost:5000/videos

3. Metadati JSON
curl http://localhost:5000/meta/<video_id>

4. Thumbnail JPEG
curl http://localhost:5000/video/<video_id>/thumb -o thumb.jpg

5. Eliminare un video
curl -X DELETE http://localhost:5000/video/<video_id>

Struttura delle chiavi Redis
Chiave	Contenuto
video:<id>	Metadati JSON
video:<id>:thumb	Thumbnail Base64
video:<id>:path	Percorso file locale
Test manuale
redis-cli
KEYS video:*
GET video:<id>

Licenza

MIT — uso libero per studio, demo e sviluppo.
