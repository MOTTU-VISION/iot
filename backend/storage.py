import json
from pathlib import Path

DATA_DIR = Path("data/records")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def save_record(camera_id, record):
    file_path = DATA_DIR / f"{camera_id}.json"
    data = []
    if file_path.exists():
        with open(file_path, "r") as f:
            data = json.load(f)

    if isinstance(record, list):
        data.extend(record)
    else:
        data.append(record)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def load_records(camera_id):
    file_path = DATA_DIR / f"{camera_id}.json"
    if file_path.exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return []
