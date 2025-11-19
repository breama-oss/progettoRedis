# Il server RESP userà questi comandi per interrogare i dati AV
import json
from database import db

def execute_command(cmd):
    if not cmd:
        return "ERROR empty command"

    name = cmd[0].upper()

    if name == "PING":
        return "PONG"

    if name == "SET" and len(cmd) == 3:
        return db.set(cmd[1], cmd[2])

    if name == "GET" and len(cmd) == 2:
        val = db.get(cmd[1])
        return val if val is not None else None

    if name == "DEL" and len(cmd) >= 2:
        return sum(db.delete(key) for key in cmd[1:])

    # AV-specific commands
    if name == "GETMETA" and len(cmd) == 2:
        meta = db.get_json(cmd[1])
        return json.dumps(meta) if meta is not None else None

    if name == "GETMETAFIELD" and len(cmd) == 3:
        meta = db.get_json(cmd[1])
        if meta is None:
            return None
        return meta.get(cmd[2])

    if name == "GETTHUMB" and len(cmd) == 2:
        # thumbnail stored under key + ":thumb"
        thumb = db.get(cmd[1] + ":thumb")
        return thumb if thumb is not None else None

    if name == "LISTVIDEOS":
        # returns array of keys like video:<uuid>
        keys = db.keys("video:")
        return keys

    return f"ERROR unknown command {name}"
