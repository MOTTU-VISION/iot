from storage import load_records

def check_alerts(known_plates):
    alerts = []
    for cam_id in range(1, 5):  # cameras 1 a 4
        records = load_records(f"camera{cam_id}")
        for rec in records:
            if rec["placa"] not in known_plates:
                alerts.append({
                    "camera_id": rec["camera_id"],
                    "placa": rec["placa"],
                    "timestamp": rec["timestamp"],
                    "alert": "Placa não cadastrada"
                })
    return alerts
