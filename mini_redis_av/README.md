### Mini Redis AV Server Python + Flask + Redis + FFmpeg

Mini Redis AV Server è un progetto didattico che consente di caricare file video, analizzarli tramite FFmpeg/ffprobe, generare thumbnail, salvare i metadati in Redis ed esporre una semplice interfaccia web e API REST tramite Flask.



  

## Funzionalità principali

  

- Caricare file video

- Estrarre metadata tramite ffprobe

- Generare thumbnail JPEG tramite ffmpeg

- Salvare i dati in Redis (reale)

- Esporre API REST

- Fornire una dashboard HTML minimale

---

## Requisiti

Assicurati di avere installato:

1. Python	≥ 3.9

Per verificare:

```bash
python3 --version
```

2. Redis	≥ 7.0

```bash
redis-cli ping
```

3. FFmpeg ≥ 4.0

```bash	
ffmpeg -version
```

4. pip	

```bash
pip --version
```

---


## Installazione

1. Clona il progetto

```bash
git clone https://github.com/breama-oss/progettoRedis.git

cd progettoRedis
```

2. Crea ambiente virtuale

*macOS / Linux*

```bash
python3 -m venv venv

source venv/bin/activate
```

*Windows (PowerShell)*

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Installa le dipendenze Python

```bash
pip install -r requirements.txt
```

4. Installa Redis

*Windows (consigliato: WSL2)*

  

Redis non è supportato nativamente su Windows.

Si consiglia WSL2 + Ubuntu.

  

- Apri PowerShell come amministratore:

```bash
wsl --install
```

Riavvia Windows se richiesto.

- Avvia Ubuntu:

```bash
wsl
```

- Installa Redis:

```bash
sudo apt update

sudo apt install redis-server
```


- Avvia:

```bash
sudo service redis-server start
```


- Test:

```bash
redis-cli ping
```

Dovresti ottenere:

```bash
PONG
```

*macOS (Homebrew)*

- Installazione:

```bash
brew install redis

brew services start redis
```


- Test:

```bash
redis-cli ping
```

Dovresti ottenere:

```bash
PONG
```

---

## Architettura del progetto


mini_redis_av/
│── av_processor.py        
│── commands.py       
│── database.py           
│── templates/
│     ├── index.html
│     ├── upload.html
│     └── video\_view.html
│── uploads/
│── http_server.py       
│── README.md
│── requirements.txt        
│── resp.py    
│── server.py        


---

## Avvio del Server

Assicurati che Redis sia attivo, poi:

*macOS / Linux*

```bash
source venv/bin/activate
cd mini_redis_av
python3 http_server.py
```


*Windows PowerShell*

```bash
.\venv\Scripts\Activate.ps1
cd mini_redis_av
python.exe http_server.py
```

Server attivo su:

```bash
http://127.0.0.1:5000
```

La homepage mostra:

elenco video caricati

thumbnail 

metadata 

pulsante elimina

---

# Upload tramite web UI
```bash
http://localhost:5000/upload_form
```

Oppure cliccando il pulsante "Carica"

---

# API REST

1. Caricare un video

```bash
curl -F "file=@/percorso/video.mp4" http://localhost:5000/upload_form
```

Risposta:

```bash
{

  "key": "video:<uuid>",

  "meta": { ... }

}
```

2. Lista di tutti i video

```bash
curl http://localhost:5000/videos
```

3. Metadati JSON formattati

```bash
curl http://localhost:5000/meta/<video_id>
```

4. Thumbnail JPEG

```bash
curl http://localhost:5000/video/<uuid>/thumb -o thumb.jpg
```

5. Eliminare un video

```bash
curl -X DELETE http://localhost:5000/video/<uuid>
```

Risposta:

```bash
{
  "deleted_keys": 3,
  "video_id": "<uuid>"
}
```

---

## Struttura delle chiavi Redis

Ogni video genera:

Chiave	Contenuto
video:<uuid>	Metadata JSON
video:<uuid>:thumb	Thumbnail Base64
video:<uuid>:path	Percorso file locale

---

## Licenza

**MIT** — libero uso per studio e sviluppo.