  

\## Descrizione generale

  

Mini Redis AV Server è un progetto didattico che consente di caricare file video, analizzarli tramite FFmpeg/ffprobe, generare thumbnail, salvare i metadati in Redis ed esporre una semplice interfaccia web e API REST tramite Flask.



  

✨ Funzionalità principali

  

📤 Caricare file video

  

🧪 Estrarre metadata tramite ffprobe

  

🖼️ Generare thumbnail JPEG tramite ffmpeg

  

🗄️ Salvare dati in Redis

  

🌐 Esporre API REST

  

🖥️ Offrire una dashboard HTML minimale

  

🧰 Requisiti

Componente Versione minima Verifica

Python ≥ 3.9 python3 --version

Redis ≥ 7.0 redis-cli ping

FFmpeg ≥ 4.0 ffmpeg -version

pip + venv sì pip --version

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

.\\venv\\Scripts\\Activate.ps1

  

3️⃣ Installa le dipendenze Python

pip install -r requirements.txt

  

4️⃣ Installa Redis

🪟 Windows (consigliato: WSL2)

  

Redis non è supportato nativamente su Windows.

Si consiglia WSL2 + Ubuntu.

  

Installa WSL2

  

wsl --install

  

  

Avvia Ubuntu:

  

wsl

  

  

Installa Redis

  

sudo apt update

sudo apt install redis-server

sudo service redis-server start

redis-cli ping

  

  

Risposta attesa:

  

PONG

  

🍏 macOS (Homebrew)

brew install redis

brew services start redis

redis-cli ping

  

🧩 Architettura del progetto

mini\_redis\_av/

│── http\_server.py        # Server Flask con API e UI

│── av\_processor.py       # ffprobe + ffmpeg + Base64 thumbnail

│── database.py           # Wrapper Redis

│── templates/

│     ├── index.html

│     ├── upload.html

│     └── video\_view.html

│── uploads/

  

▶️ Avvio del Server

macOS / Linux

source venv/bin/activate

cd mini\_redis\_av

python3 http\_server.py

  

Windows PowerShell

.\\venv\\Scripts\\Activate.ps1

cd mini\_redis\_av

python.exe http\_server.py

  

  

Server attivo su:

  

http://127.0.0.1:5000

  

🌐 Interfaccia Web

🏠 Homepage

http://localhost:5000/

  

  

Mostra:

  

elenco video caricati

  

thumbnail

  

metadata

  

pulsante elimina

  

📤 Upload tramite Web UI

http://localhost:5000/upload\_form

  

📡 API REST

1️⃣ Caricare un video

curl -F "file=@/percorso/video.mp4" http://localhost:5000/upload\_form

  

  

Risposta:

  

{

  "key": "video:<uuid>",

  "meta": { ... }

}

  

2️⃣ Lista video

curl http://localhost:5000/videos

  

3️⃣ Metadati JSON

curl http://localhost:5000/meta/<video\_id>

  

4️⃣ Thumbnail JPEG

curl http://localhost:5000/video/<uuid>/thumb -o thumb.jpg

  

5️⃣ Eliminare un video

curl -X DELETE http://localhost:5000/video/<uuid>

  

  

Risposta:

  

{

  "deleted\_keys": 3,

  "video\_id": "<uuid>"

}

  

🗄️ Struttura delle chiavi Redis

Chiave Contenuto

video:<uuid> Metadata JSON

video:<uuid>:thumb Thumbnail in Base64

video:<uuid>:path Percorso file locale

🧪 Test Manuale Completo

  

Avvia Flask

  

Carica un video con curl

  

Apri http://localhost:5000/

  

Verifica thumbnail e metadata

  

Controlla Redis:

  

redis-cli

\> KEYS video:\*

\> GET video:<uuid>

  

📜 Licenza

  

MIT — utilizzo libero per studio, demo e sviluppo.

\- estrarre metadati audiovisivi,

\- generare miniature JPEG,

\- archiviare informazioni nel database Redis,

\- visualizzare e gestire video attraverso una dashboard essenziale,

\- interagire via API con un backend leggero e facilmente estendibile.

  

L’obiettivo è fornire un progetto chiaro, portabile e comprensibile per chi desidera imparare a integrare Flask + Redis + FFmpeg.
