"""Entry point for the gesture-controlled calculator."""

import math
import time

import cv2
import numpy as np

from calculator_ui import CalculatorUI
from config import (
    CLICK_DEBOUNCE_SECONDS,
    PINCH_RELEASE_MULTIPLIER,
    PINCH_REQUIRED_FRAMES,
    PINCH_DISTANCE_THRESHOLD,
)
from expression_evaluator import ExpressionEvaluator
from hand_tracker import HandTracker


class GestureCalculatorApp:
    """Coordinates camera input, gesture clicks, calculator state, and cleanup."""

    def __init__(self) -> None:
        """Create owned components and initialize debounce state without global state."""
        self.capture = cv2.VideoCapture(0)
        self.hand_tracker = HandTracker()
        self.calculator_ui = CalculatorUI()
        self.evaluator = ExpressionEvaluator()
        self.click_detected = False
        self.last_click_time = 0.0
        self.pinch_frames = 0

    def get_frame(self) -> bytes:
        """Process one webcam frame and return it as a JPEG byte string."""
        if not self.capture.isOpened():
            raise RuntimeError("Unable to open webcam. Check that a camera is connected.")
        success, frame = self.capture.read()
        if not success:
            raise RuntimeError("Unable to read a frame from the webcam.")
        frame = cv2.flip(frame, 1)
        self._process_gesture(frame)
        self.calculator_ui.draw(frame, self.evaluator.expression)
        success, encoded_frame = cv2.imencode(".jpg", frame)
        if not success:
            raise RuntimeError("Unable to encode webcam frame as JPEG.")
        return encoded_frame.tobytes()

    def close(self) -> None:
        """Release webcam and hand-tracking resources safely and only once."""
        if self.capture.isOpened():
            self.capture.release()
        self.hand_tracker.close()

    def _process_gesture(self, frame: np.ndarray) -> bool:
        """Turn a pinched fingertip pair into at most one debounced button click."""
        fingertips = self.hand_tracker.get_fingertips(frame)
        if fingertips is None:
            self.pinch_frames = 0
            return False
        index, middle = fingertips
        midpoint = ((index[0] + middle[0]) // 2, (index[1] + middle[1]) // 2)
        cv2.line(frame, index, middle, (80, 220, 120), 2)
        cv2.circle(frame, index, 8, (80, 220, 120), -1)
        cv2.circle(frame, middle, 8, (80, 220, 120), -1)
        cv2.circle(frame, midpoint, 5, (0, 255, 255), -1)
        distance = math.hypot(index[0] - middle[0], index[1] - middle[1])
        pinch_threshold = PINCH_DISTANCE_THRESHOLD * frame.shape[1] / 640
        if not self._is_new_pinch(distance, pinch_threshold):
            return False
        return self._handle_click(midpoint)

    def _is_new_pinch(self, distance: float, pinch_threshold: float) -> bool:
        """Check threshold and debounce conditions before accepting a pinch."""
        if distance < pinch_threshold:
            self.pinch_frames += 1
        elif distance > pinch_threshold * PINCH_RELEASE_MULTIPLIER:
            self.pinch_frames = 0
            self.click_detected = False
        if self.pinch_frames < PINCH_REQUIRED_FRAMES:
            return False
        is_ready = time.time() - self.last_click_time > CLICK_DEBOUNCE_SECONDS
        if not self.click_detected and is_ready:
            self.click_detected = True
            self.last_click_time = time.time()
            return True
        return False

    def _handle_click(self, point: tuple[int, int]) -> bool:
        """Apply the calculator action selected by a gesture point."""
        button = self.calculator_ui.button_at(point)
        if button is None:
            return False
        if button.label == "CLR":
            self.evaluator.clear()
        elif button.label == "=":
            self.evaluator.evaluate()
        else:
            self.evaluator.append(button.label)
        return False