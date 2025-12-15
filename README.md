# Mini Redis AV Server Python + Flask + Redis + FFmpeg

Mini Redis AV Server è un progetto didattico che consente di caricare file video, analizzarli tramite FFmpeg/ffprobe, generare thumbnail, salvare i metadati in Redis ed esporre una semplice interfaccia web e API REST tramite Flask.



  

## Funzionalità principali

  

- Caricare file video

- Estrarre metadata tramite ffprobe

- Generare thumbnail JPEG tramite ffmpeg

- Salvare i dati in Redis (reale)

- Esporre API REST

- Fornire una dashboard HTML minimale


## Prerequisiti

Puoi avviare il progetto interamente con Docker e Docker Compose, senza installare manualmente Python, Redis o FFmpeg sul tuo sistema.

Assicurati di avere installato:

- [Docker](https://docs.docker.com/get-docker/) ≥ 24  
- [Docker Compose](https://docs.docker.com/compose/install/) (di solito incluso con Docker Desktop)



## Installazione

1. Clona il progetto

```bash
git clone https://github.com/breama-oss/progettoRedis.git

cd progettoRedis/mini_redis_av
```

2. Dopo aver aperto Docker Desktop, avvia Docker Compose:

```bash
docker-compose up -d --build
```

Questo comando:

- Costruisce l’immagine del server Flask (av_processor) con tutte le dipendenze Python e FFmpeg

- Avvia il container Redis (redis_av)

- Avvia il container Flask/mini-server RESP (av_processor)

- Espone le porte:

      - 5001 → interfaccia web e API Flask

      - 6379 → Redis (solo se mappata sull’host, altrimenti accessibile internamente dai container)

Se la porta 5001 è occupata, puoi cambiarla nel docker-compose.yml.



## Accesso all'app

Dopo pochi secondi, il server Flask sarà raggiungibile sul tuo host:

```bash
http://localhost:5001/
```

**Controllo dei log**

```bash
docker-compose logs -f
```

**Arresto dei servizi**
```bash
docker-compose down
```

I file nella cartella uploads/ rimangono intatti.


## Architettura del progetto
```bash
mini_redis_av/
│── http_server.py        # Server Flask con API e UI
│── av_processor.py       # ffprobe + ffmpeg + Base64 thumb
│── database.py           # Wrapper per Redis
│── templates/
│     ├── index.html
│     ├── upload.html
│     └── video_view.html
│── uploads/
```

## Upload tramite web UI
```bash
http://localhost:5001/upload_form
```

Oppure cliccando il pulsante "Carica"


## API REST

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


## Struttura delle chiavi Redis

Ogni video genera:
```bash
Chiave | Contenuto
video:<uuid> | Metadata JSON
video:<uuid>:thumb | Thumbnail Base64
video:<uuid>:path |	Percorso file locale
```

## Licenza

**MIT** — libero uso per studio e sviluppo.
