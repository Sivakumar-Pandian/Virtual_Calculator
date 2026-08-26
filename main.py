"""Entry point for the gesture-controlled calculator."""

import math
import time

import cv2
import numpy as np

from calculator_ui import CalculatorUI
from config import (
    BLACK,
    CLICK_DEBOUNCE_SECONDS,
    EXIT_KEY,
    EXPRESSION_FONT_SCALE,
    EXPRESSION_POSITION,
    FONT_THICKNESS,
    PINCH_DISTANCE_THRESHOLD,
    WINDOW_TITLE,
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

    def run(self) -> None:
        """Run the webcam loop and always release native resources on exit."""
        try:
            if not self.capture.isOpened():
                raise RuntimeError("Unable to open webcam. Check that a camera is connected.")
            while self._process_frame():
                pass
        except Exception as error:
            print(f"Error: {error}")
        finally:
            self.capture.release()
            self.hand_tracker.close()
            cv2.destroyAllWindows()

    def _process_frame(self) -> bool:
        """Process and display one frame, returning False when the app should stop."""
        success, frame = self.capture.read()
        if not success:
            return False
        frame = cv2.flip(frame, 1)
        if self._process_gesture(frame):
            return False
        self.calculator_ui.draw(frame)
        cv2.putText(
            frame,
            self.evaluator.expression,
            EXPRESSION_POSITION,
            cv2.FONT_HERSHEY_SIMPLEX,
            EXPRESSION_FONT_SCALE,
            BLACK,
            FONT_THICKNESS,
        )
        cv2.imshow(WINDOW_TITLE, frame)
        return cv2.waitKey(1) != EXIT_KEY

    def _process_gesture(self, frame: np.ndarray) -> bool:
        """Turn a pinched fingertip pair into at most one debounced button click."""
        fingertips = self.hand_tracker.get_fingertips(frame)
        if fingertips is None:
            return False
        index, middle = fingertips
        distance = math.hypot(index[0] - middle[0], index[1] - middle[1])
        if not self._is_new_pinch(distance):
            return False
        midpoint = ((index[0] + middle[0]) // 2, (index[1] + middle[1]) // 2)
        return self._handle_click(midpoint)

    def _is_new_pinch(self, distance: float) -> bool:
        """Check threshold and debounce conditions before accepting a pinch."""
        is_ready = time.time() - self.last_click_time > CLICK_DEBOUNCE_SECONDS
        if distance < PINCH_DISTANCE_THRESHOLD and not self.click_detected and is_ready:
            self.click_detected = True
            self.last_click_time = time.time()
            return True
        if distance > PINCH_DISTANCE_THRESHOLD:
            self.click_detected = False
        return False

    def _handle_click(self, point: tuple[int, int]) -> bool:
        """Apply a button action and return whether the Close button was pressed."""
        button = self.calculator_ui.button_at(point)
        if button is None:
            return False
        if button.label == "C":
            self.evaluator.clear()
        elif button.label == "=":
            self.evaluator.evaluate()
        elif button.label == "Close":
            return True
        else:
            self.evaluator.append(button.label)
        return False


if __name__ == "__main__":
    GestureCalculatorApp().run()