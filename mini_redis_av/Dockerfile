FROM python:3.11-slim

# install ffmpeg / ffprobe
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# directory per upload
RUN mkdir -p uploads

ENV FLASK_ENV=development
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

EXPOSE 5000
EXPOSE 6379

# avvia sia server RESP che Flask
CMD ["sh", "-c", "python server.py & python http_server.py"]
