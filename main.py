"""Connect hand tracking, calculator state, and frame rendering."""

import math
import time
from dataclasses import dataclass

import cv2
import numpy as np

from calculator_ui import button_at, draw_calculator
from config import (
    CLICK_DEBOUNCE_SECONDS,
    PINCH_RELEASE_MULTIPLIER,
    PINCH_REQUIRED_FRAMES,
    PINCH_DISTANCE_THRESHOLD,
)
from expression_evaluator import evaluate_expression
from hand_tracker import HandTrackingState, close_hand_tracker, create_hand_tracker, get_fingertips


@dataclass
class CalculatorState:
    """All mutable values needed while processing the frame stream."""

    hand_tracker: HandTrackingState
    expression: str = ""
    pinch_frames: int = 0
    pinch_active: bool = False
    last_click_time: float = 0.0


def create_calculator() -> CalculatorState:
    """Create the application state once when Flask starts."""
    return CalculatorState(hand_tracker=create_hand_tracker())


def process_frame(state: CalculatorState, frame: np.ndarray) -> bytes:
    """Process one uploaded frame and return the rendered JPEG bytes."""
    frame = cv2.flip(frame, 1)
    process_gesture(state, frame)
    draw_calculator(frame, state.expression)
    success, encoded_frame = cv2.imencode(".jpg", frame)
    if not success:
        raise RuntimeError("Unable to encode webcam frame as JPEG.")
    return encoded_frame.tobytes()


def process_gesture(state: CalculatorState, frame: np.ndarray) -> None:
    """Turn a pinched fingertip pair into at most one button click."""
    fingertips = get_fingertips(state.hand_tracker, frame)
    if fingertips is None:
        state.pinch_frames = 0
        state.pinch_active = False
        return
    index, middle = fingertips
    midpoint = ((index[0] + middle[0]) // 2, (index[1] + middle[1]) // 2)
    cv2.line(frame, index, middle, (80, 220, 120), 2)
    cv2.circle(frame, index, 8, (80, 220, 120), -1)
    cv2.circle(frame, middle, 8, (80, 220, 120), -1)
    cv2.circle(frame, midpoint, 5, (0, 255, 255), -1)
    distance = math.hypot(index[0] - middle[0], index[1] - middle[1])
    pinch_threshold = PINCH_DISTANCE_THRESHOLD * frame.shape[1] / 640
    if not is_new_pinch(state, distance, pinch_threshold):
        return
    handle_click(state, midpoint)


def is_new_pinch(state: CalculatorState, distance: float, pinch_threshold: float) -> bool:
    """Return True only once for a held pinch, after debounce checks."""
    if distance < pinch_threshold:
        state.pinch_frames += 1
    elif distance > pinch_threshold * PINCH_RELEASE_MULTIPLIER:
        state.pinch_frames = 0
        state.pinch_active = False
    if state.pinch_frames < PINCH_REQUIRED_FRAMES:
        return False
    is_ready = time.time() - state.last_click_time > CLICK_DEBOUNCE_SECONDS
    if not state.pinch_active and is_ready:
        state.pinch_active = True
        state.last_click_time = time.time()
        return True
    return False


def handle_click(state: CalculatorState, point: tuple[int, int]) -> None:
    """Apply the calculator action selected by the gesture point."""
    button = button_at(point)
    if button is None:
        return
    if button.label == "CLR":
        state.expression = ""
    elif button.label == "=":
        state.expression = evaluate_expression(state.expression)
    else:
        state.expression += button.label


def close_calculator(state: CalculatorState) -> None:
    """Release MediaPipe resources when the server exits."""
    close_hand_tracker(state.hand_tracker)