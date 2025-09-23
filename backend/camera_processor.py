import cv2
import time
from storage import save_record
from vision import analyze_frame

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
            save_record(camera_id, record)

        time.sleep(0.2)

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop infinito
            continue
        yield frame