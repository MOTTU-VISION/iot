import time
from storage import (
    load_records,
    get_all_known_plates,
    save_alert,
    load_alerts,
    delete_alert
)

ALERT_TYPES = {
    "PLACA_DESCONHECIDA": "Veículo não cadastrado",
    "MOTO_NAO_LOCALIZADA": "Moto cadastrada não localizada em câmeras"
}

def check_unregistered_plates():
    """Gera alertas para placas detectadas que não estão na tabela moto"""
    known_plates = get_all_known_plates()
    cameras = ["camera1", "camera2", "camera3", "camera4"]

    for cam_id in cameras:
        registros = load_records(cam_id)
        for rec in registros:
            if rec["placa"] not in known_plates:
                alert = {
                    "camera_id": cam_id,
                    "placa": rec["placa"],
                    "timestamp": rec["timestamp"],
                    "alert": ALERT_TYPES["PLACA_DESCONHECIDA"],
                    "severity": "medium"
                }
                save_alert(alert)


def check_missing_motos():
    """Gera alertas para motos cadastradas que não estão sendo vistas em nenhuma câmera"""
    known_plates = get_all_known_plates()
    registros_em_camera = set()

    for cam_id in ["camera1", "camera2", "camera3", "camera4"]:
        registros = load_records(cam_id)
        for rec in registros:
            registros_em_camera.add(rec["placa"])

    for placa in known_plates:
        if placa not in registros_em_camera:
            alert = {
                "camera_id": None,
                "placa": placa,
                "timestamp": time.time(),
                "alert": ALERT_TYPES["MOTO_NAO_LOCALIZADA"],
                "severity": "medium"
            }
            save_alert(alert)


def resolve_alerts():
    """Remove alertas que já foram resolvidos"""
    alerts = load_alerts()
    known_plates = get_all_known_plates()
    registros_em_camera = {r["placa"]
                           for cam in ["camera1", "camera2", "camera3", "camera4"]
                           for r in load_records(cam)}

    for alert in alerts:
        placa = alert["placa"]
        tipo = alert["alert"]

        if tipo == ALERT_TYPES["PLACA_DESCONHECIDA"] and placa in known_plates:
            delete_alert(placa)

        elif tipo == ALERT_TYPES["MOTO_NAO_LOCALIZADA"] and placa in registros_em_camera:
            delete_alert(placa)


def run_analyzer(interval=10):
    """Loop principal de análise"""
    print("🧠 Iniciando analyzer de alertas em loop...")
    while True:
        try:
            check_unregistered_plates()
            check_missing_motos()
            resolve_alerts()
            time.sleep(interval)
        except Exception as e:
            print(f"Erro no analyzer: {e}")
            time.sleep(interval)
