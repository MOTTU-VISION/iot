import cv2
from flask_cors import CORS
from worker import start_workers
from analyzer import check_alerts
from flask import Flask, jsonify, Response
from camera_processor import generate_frames
from storage import load_records, read_records_from_file, load_alerts, read_alerts_from_file, read_all_records_from_file

app = Flask(__name__)
CORS(app, origins="*")

CAMERA_PATHS = {
    "camera1": "data/videos/camera1.mp4",
    "camera2": "data/videos/camera2.mp4",
    "camera3": "data/videos/camera3.mp4",
    "camera4": "data/videos/camera4.mp4",
}

tread_list = start_workers(CAMERA_PATHS)

@app.route("/stream/<camera_id>")
def stream(camera_id):
    def gen():
        for frame in generate_frames(CAMERA_PATHS[camera_id]):
            _, buffer = cv2.imencode('.jpg', frame)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/records/<camera_id>")
def get_records(camera_id):
    return jsonify(load_records(camera_id))

@app.route("/alerts")
def get_alerts():
    known_plates = ["JAF9344", "XYZ9999"]
    check_alerts(known_plates)
    alerts = load_alerts() #cache
    if not alerts:
        alerts = read_alerts_from_file()
    return jsonify(alerts)

@app.route("/records/file/<camera_id>")
def get_file_records(camera_id):
    records = read_records_from_file(camera_id)
    return jsonify(records), 200

@app.route("/records/file/all")
def get_all_file_records():
    records = read_all_records_from_file()
    return jsonify(records), 200

if __name__ == "__main__":
    app.run(debug=True)
