from storage import load_records, save_alerts, read_alerts_from_file, read_records_from_file


def check_alerts(known_plates):
    alerts = []
    for cam_id in range(1, 5):  # cameras 1 a 4
        records = read_records_from_file(f"camera{cam_id}")
        for rec in records:
            if rec["placa"] not in known_plates:
                alerts.append({
                    "camera_id": rec["camera_id"],
                    "placa": rec["placa"],
                    "timestamp": rec["timestamp"],
                    "alert": "Placa não cadastrada",
                    "severity": "low"
                })

    # Salvar persistência local
    if alerts:
        save_alerts(alerts)

    return alerts
