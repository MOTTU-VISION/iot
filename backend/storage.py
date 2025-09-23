# storage.py
import json
import threading
from pathlib import Path

# Diretórios de persistência
DATA_DIR = Path("data/records")
DATA_DIR.mkdir(parents=True, exist_ok=True)

ALERTS_DIR = Path("data/alerts")
ALERTS_DIR.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()
records_cache = {}  # {camera_id: [registros]}
alerts_cache = []   # lista global de alertas

# ----------------------------
# REGISTROS DE CÂMERAS
# ----------------------------
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

def read_records_from_file(camera_id):
    file_path = DATA_DIR / f"{camera_id}.json"
    if file_path.exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return []

# ----------------------------
# ALERTAS
# ----------------------------
def save_alerts(alerts):
    """Salva novos alertas no cache e em disco"""
    global alerts_cache
    with _lock:
        # evita duplicados pela combinação (placa, camera_id, timestamp)
        existing = {(a["placa"], a["camera_id"], a["timestamp"]) for a in alerts_cache}
        new_alerts = [
            a for a in alerts
            if (a["placa"], a["camera_id"], a["timestamp"]) not in existing
        ]

        if new_alerts:
            alerts_cache.extend(new_alerts)

            # persistência → em único arquivo
            file_path = ALERTS_DIR / "alerts.json"
            with open(file_path, "w") as f:
                json.dump(alerts_cache, f, indent=2)

def load_alerts():
    """Retorna alertas em memória"""
    with _lock:
        return alerts_cache

def read_alerts_from_file():
    """Carrega alertas salvos em disco"""
    file_path = ALERTS_DIR / "alerts.json"
    if file_path.exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return []
