# Accetta multipart/form-data file, 
# chiama process_and_store e restituisce video:<uuid>

import os
from flask import Flask, request, jsonify, send_file, render_template, redirect
from av_processor import process_and_store
from database import db
import io
import base64

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)

# Home page: lista di tutti i video caricati

@app.route("/")
def home():
    keys = db.keys("video:")
    vids = [k.replace("video:", "") for k in keys if k.count(":") == 1]
    return render_template("index.html", videos=vids, title="Home")

# Form per caricare video

@app.route("/upload_form", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html", title="Carica Video")
    if "file" not in request.files:
        return jsonify({"error": "missing file"}), 400

    f = request.files["file"]
    filename = f.filename or "upload"
    save_path = os.path.join(UPLOAD_DIR, filename)
    # ensure unique name if exists
    base, ext = os.path.splitext(filename)
    idx = 1
    while os.path.exists(save_path):
        save_path = os.path.join(UPLOAD_DIR, f"{base}-{idx}{ext}")
        idx += 1

    f.save(save_path)

    try:
        key, meta = process_and_store(save_path, original_filename=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"key": key, "meta": meta})

# Dettaglio video con metadata e thumbnail

@app.route("/video/<vid>/view")
def view_video(vid):
    meta = db.get_json(f"video:{vid}")
    thumb = db.get(f"video:{vid}:thumb")

    if not meta:
        return "Video non trovato", 404

    return render_template(
        "video_view.html",
        meta=meta,
        thumb=thumb,
        title="Video"
    )

# Elimina video e relative chiavi dal DB

@app.route("/video/<vid>/delete")
def delete_video_page(vid):
    prefix = f"video:{vid}"
    keys = db.keys(prefix)

    if not keys:
        return "Video non trovato", 404

    # elimina file
    file_path = db.get(prefix + ":path")
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            pass

    # elimina chiavi DB
    for k in keys:
        db.delete(k)

    return redirect("/")


# 1) ENDPOINT: RITORNA JSON FORMATTATO

@app.route("/meta/<video_id>", methods=["GET"])
def get_meta(video_id):
    key = f"video:{video_id}"
    meta = db.get_json(key)
    if meta is None:
        return jsonify({"error": "video not found"}), 404
    return jsonify(meta)



# 2) ENDPOINT: LISTA DI TUTTI I VIDEO

@app.route("/videos", methods=["GET"])
def list_videos():
    keys = db.keys("video:")
    return jsonify(keys)

# 3) ENDPOINT: RITORNA THUMBNAIL DECODIFICATO

@app.route("/video/<vid>/thumb", methods=["GET"])
def get_thumbnail(vid):
    key_thumb = f"video:{vid}:thumb"
    thumb_b64 = db.get(key_thumb)

    if not thumb_b64:
        return jsonify({"error": "thumbnail not found"}), 404

    img_bytes = base64.b64decode(thumb_b64)

    return send_file(
        io.BytesIO(img_bytes),
        mimetype="image/jpeg",
        download_name=f"{vid}.jpg"
    )

# 4) ENDPOINT: CANCELLA VIDEO VIA API

@app.route("/video/<vid>", methods=["DELETE"])
def delete_video(vid):
    prefix = f"video:{vid}"
    keys = db.keys(prefix)

    if not keys:
        return jsonify({"error": "video not found"}), 404

    # rimuovi il file fisico se presente
    file_path = db.get(prefix + ":path")
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            pass

    # elimina tutte le chiavi col prefisso
    deleted = 0
    for k in keys:
        deleted += db.delete(k)

    return jsonify({"deleted_keys": deleted, "video_id": vid})

# Avvia il server Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
