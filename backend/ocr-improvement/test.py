import cv2
import easyocr
from ultralytics import YOLO
from flask import Flask, Response

# Modelo YOLO treinado para detectar PLACAS (não veículos)
plate_model = YOLO("yolov8n.pt")
ocr_reader = easyocr.Reader(["en"])  # OCR

app = Flask(__name__)

CAMERA_PATHS = {
    "camera1": "../data/videos/camera1.mp4",
}

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop infinito
            continue

        # Detecção de placas diretamente
        results = plate_model(frame)

        for r in results:
            boxes = r.boxes.xyxy.cpu().numpy()

            for box in boxes:
                x1, y1, x2, y2 = map(int, box)

                # Recorta a placa
                plate_img = frame[y1:y2, x1:x2]

                # OCR só na placa
                text_results = ocr_reader.readtext(plate_img)

                # Concatena todos os textos detectados
                raw_text = "".join([res[1] for res in text_results]) if text_results else ""

                # Expressão regular para placas brasileiras (padrão antigo e Mercosul)
                match = re.search(r"[A-Z]{3}\d{4}|[A-Z]{3}\d[A-Z]\d{2}", raw_text.upper())

                plate_text = match.group(0) if match else "unknow"

                # Desenhar bounding box ao redor da placa
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Mostrar OCR acima da placa
                cv2.putText(
                    frame,
                    plate_text,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

        # Codifica para streaming
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route("/stream/<camera_id>")
def stream(camera_id):
    return Response(
        generate_frames(CAMERA_PATHS[camera_id]),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

if __name__ == "__main__":
    app.run(debug=True)