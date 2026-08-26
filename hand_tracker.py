"""MediaPipe hand tracking used by the calculator application."""

from typing import Optional

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


class HandTracker:
    """Finds the index and middle fingertips in webcam frames."""

    def __init__(self) -> None:
        """Create one MediaPipe Hands pipeline for the application's lifetime."""
        hands_module = mp.solutions.hands
        self._hands = hands_module.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE,
        )
        self._smoothed_fingertips: Optional[Fingertips] = None

    def get_fingertips(self, frame: np.ndarray) -> Optional[Fingertips]:
        """Return fingertip pixels, or None when no complete hand is visible."""
        height, width = frame.shape[:2]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb_frame)
        if not results.multi_hand_landmarks:
            self._smoothed_fingertips = None
            return None
        landmarks = results.multi_hand_landmarks[0].landmark
        index = landmarks[INDEX_FINGER_LANDMARK]
        middle = landmarks[MIDDLE_FINGER_LANDMARK]
        fingertips = (
            (int(index.x * width), int(index.y * height)),
            (int(middle.x * width), int(middle.y * height)),
        )
        if self._smoothed_fingertips is None:
            self._smoothed_fingertips = fingertips
            return fingertips
        previous_index, previous_middle = self._smoothed_fingertips
        smoothed = (
            self._smooth_point(previous_index, fingertips[0]),
            self._smooth_point(previous_middle, fingertips[1]),
        )
        self._smoothed_fingertips = smoothed
        return smoothed

    @staticmethod
    def _smooth_point(previous: tuple[int, int], current: tuple[int, int]) -> tuple[int, int]:
        """Reduce landmark jitter while keeping the pointer responsive."""
        return (
            int(previous[0] * FINGERTIP_SMOOTHING + current[0] * (1 - FINGERTIP_SMOOTHING)),
            int(previous[1] * FINGERTIP_SMOOTHING + current[1] * (1 - FINGERTIP_SMOOTHING)),
        )

    def close(self) -> None:
        """Release MediaPipe resources so the native pipeline shuts down cleanly."""
        self._hands.close()