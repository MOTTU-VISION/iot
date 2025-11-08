import cv2
import traceback
from flask_cors import CORS
from camera_processor import generate_frames
from flask import Flask, jsonify, Response, request
from worker import start_workers, start_worker_alert
from storage import load_records, load_alerts, save_moto, delete_alert

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

CAMERA_PATHS = {
    "camera1": "data/videos/camera2.mkv",
    "camera2": "data/videos/camera1.mkv",
    "camera3": "data/videos/camera3.mkv",
    "camera4": "data/videos/camera4.mkv",
}

tread_list = start_workers(CAMERA_PATHS)
tread_list_alerts = start_worker_alert()

@app.route("/stream/<camera_id>")
def stream(camera_id):
    def gen():
        if camera_id not in CAMERA_PATHS:
            return jsonify({"error": "Câmera não encontrada"}), 404

        for frame in generate_frames(CAMERA_PATHS[camera_id]):
            _, buffer = cv2.imencode('.jpg', frame)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/records/<camera_id>")
def get_records(camera_id):
    try:
        records = load_records(camera_id)
        return jsonify(records), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "details": str(e)
        }), 500

@app.route("/alerts")
def get_alerts():
    try:
        alerts = load_alerts() #cache
        if not alerts:
            alerts = load_alerts()
        return jsonify(alerts)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "details": str(e)
        }), 500

@app.route("/alert/<placa>", methods=['DELETE'])
def delete_alert_by_plate(placa):
    try:
        delete_alert(placa)
        return jsonify({}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "details": str(e)
        }), 500

@app.route("/moto", methods=['POST'])
def post_moto():
    try:
        data = request.json
        placa = data["placa"]
        camera = data["camera"]
        save_moto(camera, placa)
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": "Erro ao cadastrar moto.",
            "details": str(e)
        }), 500
    finally:
        return jsonify({}), 200

if __name__ == "__main__":
    app.run(debug=True)