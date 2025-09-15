import threading
from camera_processor import process_camera

def start_workers(CAMERA_PATHS):
    print("🚀 Iniciando processamento das câmeras em background...")
    threads = []
    for cam_id, path in CAMERA_PATHS.items():
        t = threading.Thread(target=process_camera, args=(cam_id, path), daemon=True)
        t.start()
        threads.append(t)
    return threads