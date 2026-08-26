"""Flask web server for the gesture-controlled calculator."""

import atexit
from typing import Iterator

from flask import Flask, Response, render_template

from main import GestureCalculatorApp

app = Flask(__name__)
calculator = GestureCalculatorApp()


def generate_frames() -> Iterator[bytes]:
    """Yield processed webcam frames in the browser's MJPEG format."""
    while True:
        try:
            frame = calculator.get_frame()
        except RuntimeError as error:
            print(f"Error: {error}")
            break
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"


def cleanup() -> None:
    """Release camera and MediaPipe resources when the server exits."""
    calculator.close()


atexit.register(cleanup)


@app.get("/")
def index() -> str:
    """Render the calculator stream page."""
    return render_template("index.html")


@app.get("/video_feed")
def video_feed() -> Response:
    """Stream processed frames as an MJPEG response."""
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True)
