"""Flask web server for the gesture-controlled calculator."""

import atexit

from flask import Flask, Response, render_template
import cv2
import numpy as np
from flask import jsonify, request

from main import GestureCalculatorApp

app = Flask(__name__)
calculator = GestureCalculatorApp()
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024


def cleanup() -> None:
    """Release camera and MediaPipe resources when the server exits."""
    calculator.close()


atexit.register(cleanup)


@app.get("/")
def index() -> str:
    """Render the calculator stream page."""
    return render_template("index.html")


@app.post("/process_frame")
def process_frame() -> Response:
    """Process one webcam frame captured by the browser."""
    uploaded_frame = request.files.get("frame")
    if uploaded_frame is None:
        return jsonify(error="No frame was uploaded."), 400
    frame = cv2.imdecode(
        np.frombuffer(uploaded_frame.read(), dtype=np.uint8), cv2.IMREAD_COLOR
    )
    if frame is None:
        return jsonify(error="The uploaded frame is not a valid image."), 400
    height, width = frame.shape[:2]
    if width > 640:
        scale = 640 / width
        frame = cv2.resize(frame, (640, int(height * scale)))
    return Response(calculator.process_frame(frame), mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True)
