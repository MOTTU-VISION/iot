import json
from pathlib import Path
import threading

DATA_DIR = Path("data/records")
DATA_DIR.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()
records_cache = {}  # {camera_id: [registros]}

def save_record(camera_id, record):
    with _lock:
        if camera_id not in records_cache:
            records_cache[camera_id] = []

        # Evita duplicados (mesma placa já vista recentemente)
        existing = {r["placa"] for r in records_cache[camera_id]}
        new_records = [r for r in record if r["placa"] not in existing]

        if new_records:
            records_cache[camera_id].extend(new_records)

            # Persistência eventual → só quando há novidade
            file_path = DATA_DIR / f"{camera_id}.json"
            with open(file_path, "w") as f:
                json.dump(records_cache[camera_id], f, indent=2)

def load_records(camera_id):
    with _lock:
        return records_cache.get(camera_id, [])
