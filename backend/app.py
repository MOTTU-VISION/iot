from camera_processor import generate_frames
from flask import Flask, jsonify, Response
from analyzer import check_alerts
from storage import  load_records
import cv2
from worker import start_workers

app = Flask(__name__)

CAMERA_PATHS = {
    "camera1": "data/videos/camera1.mp4",
    "camera2": "data/videos/camera2.mp4",
    "camera3": "data/videos/camera3.mp4",
    "camera4": "data/videos/camera4.mp4",
}
start_workers(CAMERA_PATHS)

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
    known_plates = ["ABC1234", "XYZ9999"]
    return jsonify(check_alerts(known_plates))

if __name__ == "__main__":
    app.run(debug=True)
