import cv2
from vision import analyze_frame
from storage import save_record

def process_camera(camera_id, video_path):
    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reinicia vídeo
            continue

        record = analyze_frame(frame, camera_id)
        if record:
            save_record(camera_id, record)

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop infinito
            continue
        yield frame