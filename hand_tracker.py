"""MediaPipe hand tracking used by the calculator application."""

from typing import Optional

import cv2
import mediapipe as mp
import numpy as np

from config import (
    DETECTION_CONFIDENCE,
    INDEX_FINGER_LANDMARK,
    MIDDLE_FINGER_LANDMARK,
    TRACKING_CONFIDENCE,
)

Fingertips = tuple[tuple[int, int], tuple[int, int]]


class HandTracker:
    """Finds the index and middle fingertips in webcam frames."""

    def __init__(self) -> None:
        """Create one MediaPipe Hands pipeline for the application's lifetime."""
        hands_module = mp.solutions.hands
        self._hands = hands_module.Hands(
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE,
        )

    def get_fingertips(self, frame: np.ndarray) -> Optional[Fingertips]:
        """Return fingertip pixels, or None when no complete hand is visible."""
        height, width = frame.shape[:2]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb_frame)
        if not results.multi_hand_landmarks:
            return None
        landmarks = results.multi_hand_landmarks[0].landmark
        index = landmarks[INDEX_FINGER_LANDMARK]
        middle = landmarks[MIDDLE_FINGER_LANDMARK]
        return (
            (int(index.x * width), int(index.y * height)),
            (int(middle.x * width), int(middle.y * height)),
        )

    def close(self) -> None:
        """Release MediaPipe resources so the native pipeline shuts down cleanly."""
        self._hands.close()