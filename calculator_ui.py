"""Button model and rendering logic for the calculator overlay."""

from typing import Optional

import cv2
import numpy as np

from config import (
    BLACK,
    BUTTON_CONFIGS,
    BUTTON_SIZE,
    FRAME_WEIGHT,
    FONT_THICKNESS,
    LABEL_FONT_SCALE,
    OVERLAY_WEIGHT,
    ButtonConfig,
    Position,
)


class CalculatorButton:
    """Represents a labeled, colored rectangular control on the calculator."""

    def __init__(self, config: ButtonConfig) -> None:
        """Create a button from configuration so layout stays out of UI logic."""
        self.label = config.label
        self.position = config.position
        self.size = BUTTON_SIZE
        self.color = config.color

    def contains(self, point: Position) -> bool:
        """Return whether a pixel point is inside this button's original bounds."""
        x, y = point
        button_x, button_y = self.position
        return (
            button_x < x < button_x + self.size
            and button_y < y < button_y + self.size
        )

    def draw(self, frame: np.ndarray, overlay: np.ndarray) -> None:
        """Paint the button and center its label on the overlay."""
        x, y = self.position
        cv2.rectangle(overlay, (x, y), (x + self.size, y + self.size), self.color, -1)
        label_size = cv2.getTextSize(
            self.label, cv2.FONT_HERSHEY_SIMPLEX, LABEL_FONT_SCALE, FONT_THICKNESS
        )[0]
        label_x = x + (self.size - label_size[0]) // 2
        label_y = y + (self.size + label_size[1]) // 2
        cv2.putText(
            overlay,
            self.label,
            (label_x, label_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            LABEL_FONT_SCALE,
            BLACK,
            FONT_THICKNESS,
        )


class CalculatorUI:
    """Owns calculator buttons and handles rendering and hit-testing."""

    def __init__(self, button_configs: tuple[ButtonConfig, ...] = BUTTON_CONFIGS) -> None:
        """Build button objects from configuration for a stable, testable layout."""
        self.buttons = [CalculatorButton(config) for config in button_configs]

    def draw(self, frame: np.ndarray) -> None:
        """Draw a readable calculator panel over the camera frame."""
        overlay = frame.copy()
        cv2.rectangle(overlay, (30, 25), (345, 355), (245, 248, 250), -1)
        for button in self.buttons:
            button.draw(frame, overlay)
        cv2.addWeighted(overlay, OVERLAY_WEIGHT, frame, FRAME_WEIGHT, 0, frame)
        cv2.rectangle(frame, (30, 25), (345, 355), (255, 255, 255), 2)

    def button_at(self, point: Position) -> Optional[CalculatorButton]:
        """Return the first button containing a point, preserving layout order."""
        return next((button for button in self.buttons if button.contains(point)), None)