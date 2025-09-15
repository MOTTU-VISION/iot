import threading
from camera_processor import process_camera

CAMERA_PATHS = {
    "camera1": "data/videos/camera1.mp4",
    "camera2": "data/videos/camera2.mp4",
    "camera3": "data/videos/camera3.mp4",
    "camera4": "data/videos/camera4.mp4",
}

def start_workers():
    threads = []
    for cam_id, path in CAMERA_PATHS.items():
        t = threading.Thread(target=process_camera, args=(cam_id, path), daemon=True)
        t.start()
        threads.append(t)
    return threads

if __name__ == "__main__":
    print("🚀 Iniciando processamento das câmeras em background...")
    start_workers()

    # Mantém a thread principal viva
    while True:
        pass
