import threading
from analyzer import run_analyzer
from camera_processor import process_camera

# Função que cria threads especificas para cada camera
def start_workers(CAMERA_PATHS):
    print("🚀 Iniciando processamento das câmeras em background...")
    threads = []
    for cam_id, path in CAMERA_PATHS.items():
        t = threading.Thread(target=process_camera, args=(cam_id, path), daemon=True)
        t.start()
        threads.append(t)
    return threads

# Função que cria threads para analisar e gerenciar alertas
def start_worker_alert(interval=20):
    from analyzer import run_analyzer
    print("🚀 Iniciando analyzer em background...")
    t = threading.Thread(target=run_analyzer, args=(interval,), daemon=True)
    t.start()
    return [t]
