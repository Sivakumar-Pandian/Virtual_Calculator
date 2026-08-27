"""Small functions for detecting and smoothing two fingertip positions."""

from dataclasses import dataclass
from typing import Any

import cv2
import mediapipe as mp
import numpy as np

from config import (
    DETECTION_CONFIDENCE,
    FINGERTIP_SMOOTHING,
    INDEX_FINGER_LANDMARK,
    MIDDLE_FINGER_LANDMARK,
    TRACKING_CONFIDENCE,
)

Fingertips = tuple[tuple[int, int], tuple[int, int]]


@dataclass
class HandTrackingState:
    """MediaPipe pipeline and the previous points used for smoothing."""

    hands: Any
    previous_fingertips: Fingertips | None = None


def create_hand_tracker() -> HandTrackingState:
    """Create one MediaPipe pipeline for the application's lifetime."""
    hands = mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        model_complexity=0,
        min_detection_confidence=DETECTION_CONFIDENCE,
        min_tracking_confidence=TRACKING_CONFIDENCE,
    )
    return HandTrackingState(hands=hands)


def get_fingertips(state: HandTrackingState, frame: np.ndarray) -> Fingertips | None:
    """Return index and middle fingertip pixels, or None without a hand."""
    height, width = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = state.hands.process(rgb_frame)
    if not results.multi_hand_landmarks:
        state.previous_fingertips = None
        return None

    landmarks = results.multi_hand_landmarks[0].landmark
    current = (
        (int(landmarks[INDEX_FINGER_LANDMARK].x * width), int(landmarks[INDEX_FINGER_LANDMARK].y * height)),
        (int(landmarks[MIDDLE_FINGER_LANDMARK].x * width), int(landmarks[MIDDLE_FINGER_LANDMARK].y * height)),
    )
    if state.previous_fingertips is None:
        state.previous_fingertips = current
        return current

    previous_index, previous_middle = state.previous_fingertips
    smoothed = (_smooth_point(previous_index, current[0]), _smooth_point(previous_middle, current[1]))
    state.previous_fingertips = smoothed
    return smoothed


def _smooth_point(previous: tuple[int, int], current: tuple[int, int]) -> tuple[int, int]:
    """Reduce landmark jitter while keeping the pointer responsive."""
    return (
        int(previous[0] * FINGERTIP_SMOOTHING + current[0] * (1 - FINGERTIP_SMOOTHING)),
        int(previous[1] * FINGERTIP_SMOOTHING + current[1] * (1 - FINGERTIP_SMOOTHING)),
    )


def close_hand_tracker(state: HandTrackingState) -> None:
    """Release MediaPipe's native resources."""
    state.hands.close()