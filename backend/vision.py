from ultralytics import YOLO
import easyocr
import time

# Carregar modelo pré-treinado YOLOv8 para detectar veículos e placas
yolo_model = YOLO("yolov8n.pt")  # pode trocar por yolov8s.pt para mais precisão
ocr_reader = easyocr.Reader(["en"])

def analyze_frame(frame, camera_id):
    results = yolo_model(frame)
    records = []

    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy()
        cls = r.boxes.cls.cpu().numpy()

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box)
            label = int(cls[i])

            # Exemplo: se for veículo (classe 2 = carro, 3 = moto, depende do dataset)
            if label in [2, 3, 5, 7]:  # carro, moto, ônibus, caminhão
                vehicle_img = frame[y1:y2, x1:x2]

                # OCR na região do veículo (simplificação: aplicando OCR no veículo inteiro)
                text = ocr_reader.readtext(vehicle_img)
                plate = text[0][1] if text else "UNKNOWN"

                records.append({
                    "camera_id": camera_id,
                    "timestamp": time.time(),
                    "placa": plate,
                    "bounding_box": [x1, y1, x2, y2],
                    "label": str(label)
                })

    # Se detectou múltiplos veículos, retorna todos
    return records if records else None
