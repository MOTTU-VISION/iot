import cv2
import time
from vision import analyze_frame
from storage import save_record, delete_record_by_plate, load_records, save_moto, get_all_known_plates, save_alert

## Função que analisa os frames
def process_camera(camera_id, video_path, frame_skip=5):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia vídeo
            continue

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        record = analyze_frame(frame, camera_id)
        if record:
            for r in record:
                # Se essa placa já estava em outra câmera, remover
                all_cameras = ["camera1", "camera2", "camera3", "camera4"]
                for cam in all_cameras:
                    if cam != camera_id:
                        registros = load_records(cam)
                        if any(x["placa"] == r["placa"] for x in registros):
                            delete_record_by_plate(r["placa"])
                save_record(camera_id, [r])

                known_plates = get_all_known_plates()

                if r["placa"] not in known_plates:
                    alert ={
                        "camera_id": r["camera_id"],
                        "placa": r["placa"],
                        "timestamp": r["timestamp"],
                        "alert": "Placa não cadastrada no banco",
                        "severity": "medium"
                    }
                    save_alert(alert)

        time.sleep(2)

## Função que gera o stream das cameras
def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop infinito
            continue
        yield frame