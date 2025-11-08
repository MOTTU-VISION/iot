import re
import time
import easyocr
from ultralytics import YOLO

# Carregar modelo pré-treinado YOLOv8 para detectar veículos e placas
yolo_model = YOLO("yolov8n.pt")  # pode trocar por yolov8s.pt para mais precisão
ocr_reader = easyocr.Reader(["en"])

## Retorna um registro ao extrair e validar uma placa
def analyze_frame(frame, camera_id):
    results = yolo_model(frame, stream=True)
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

                try:
                    # OCR na região do veículo (simplificação: aplicando OCR no veículo inteiro)
                    text = ocr_reader.readtext(vehicle_img)
                except Exception as e:
                    print(str(e))

                # Concatena todos os textos detectados
                raw_text = "".join([res[1] for res in text]) if text else ""

                # Expressão regular para placas brasileiras (padrão antigo e Mercosul)
                match = re.search(r"[A-Z]{3}\d{4}|[A-Z]{3}\d[A-Z]\d{2}", raw_text.upper())

                plate = match.group(0) if match else "UNKNOWN"

                if plate != "UNKNOWN":
                    records.append({
                        "camera_id": camera_id,
                        "timestamp": time.time(),
                        "placa": plate,
                        "bounding_box": [x1, y1, x2, y2],
                        "label": str(label)
                    })

    # Se detectou múltiplos veículos, retorna todos
    return records if records else None
