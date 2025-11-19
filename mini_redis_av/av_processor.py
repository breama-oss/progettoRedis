# Salva thumbnail in base64 e metadata JSON estratti con ffprobe
import subprocess
import json
import os
import base64
import uuid
from database import db

def run_ffprobe(path):
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        path
    ]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {p.stderr.decode('utf-8')}")
    return json.loads(p.stdout.decode('utf-8'))

def make_thumbnail(path, out_path, time="00:00:01"):
    # creates a single-frame thumbnail at given time (format HH:MM:SS or seconds)
    cmd = [
        "ffmpeg", "-y", "-ss", time, "-i", path,
        "-frames:v", "1",
        "-q:v", "2",
        out_path
    ]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg thumbnail failed: {p.stderr.decode('utf-8')}")

def encode_file_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode('ascii')

def extract_device_info(info):
    device = {
        "make": None,
        "model": None,
        "software": None
    }

    fmt = info.get("format", {})
    tags = fmt.get("tags", {})

    # Apple (iPhone/iPad)
    device["make"] = (
        tags.get("com.apple.quicktime.make") or
        tags.get("make")
    )
    device["model"] = (
        tags.get("com.apple.quicktime.model") or
        tags.get("model")
    )
    device["software"] = (
        tags.get("com.apple.quicktime.software") or
        tags.get("software")
    )

    # Android (Samsung, Xiaomi, ecc)
    # spesso usano "make" e "model" direttamente
    if not device["make"]:
        device["make"] = tags.get("make")

    if not device["model"]:
        device["model"] = tags.get("model")

    return device

def process_and_store(file_path, original_filename=None):
    """
    Extract metadata via ffprobe, generate thumbnail, store JSON metadata and thumb in DB.
    Returns assigned video key.
    """
    info = run_ffprobe(file_path)

    device_info = extract_device_info(info)

    meta = {
        "original_filename": original_filename,
        "format": info.get("format"),
        "streams": info.get("streams"),
        "device": device_info
    }

    # create unique id
    vid = str(uuid.uuid4())
    key = f"video:{vid}"

    # thumbnail path
    thumb_path = f"{file_path}.thumb.jpg"
    try:
        # try to use 1 second as thumbnail time; if duration shorter may fail but ffmpeg often handles
        make_thumbnail(file_path, thumb_path, time="00:00:01")
        thumb_b64 = encode_file_base64(thumb_path)
    except Exception as e:
        thumb_b64 = None

    # store metadata and thumb
    db.set_json(key, meta)
    if thumb_b64:
        db.set(key + ":thumb", thumb_b64)

    # also store a pointer to the original filename path (optional)
    db.set(key + ":path", file_path)

    # cleanup thumbnail file
    try:
        if os.path.exists(thumb_path):
            os.remove(thumb_path)
    except:
        pass

    return key, meta

