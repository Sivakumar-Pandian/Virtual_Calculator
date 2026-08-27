"""Button hit-testing and drawing for the calculator overlay."""

import cv2
import numpy as np

from config import (
    BLACK,
    BUTTON_CONFIGS,
    BUTTON_SIZE,
    EXPRESSION_FONT_SCALE,
    EXPRESSION_POSITION,
    FONT_THICKNESS,
    LABEL_FONT_SCALE,
    WHITE,
    ButtonConfig,
    Position,
)


def button_at(point: Position) -> ButtonConfig | None:
    """Return the button containing a point, or None outside the layout."""
    x, y = point
    for button in BUTTON_CONFIGS:
        button_x, button_y = button.position
        if button_x < x < button_x + BUTTON_SIZE and button_y < y < button_y + BUTTON_SIZE:
            return button
    return None


def draw_calculator(frame: np.ndarray, expression: str = "") -> None:
    """Draw the calculator and current expression over a camera frame."""
    overlay = frame.copy()
    cv2.rectangle(overlay, (28, 22), (334, 382), (22, 31, 37), -1)
    cv2.rectangle(overlay, (45, 42), (317, 94), (8, 14, 18), -1)
    for button in BUTTON_CONFIGS:
        draw_button(overlay, button)
    cv2.addWeighted(overlay, 0.88, frame, 0.12, 0, frame)
    cv2.rectangle(frame, (28, 22), (334, 382), (141, 214, 194), 2)
    cv2.rectangle(frame, (45, 42), (317, 94), (76, 105, 111), 1)
    cv2.putText(frame, (expression or "0")[-24:], EXPRESSION_POSITION,
                cv2.FONT_HERSHEY_SIMPLEX, EXPRESSION_FONT_SCALE,
                (245, 250, 247), FONT_THICKNESS)


def draw_button(frame: np.ndarray, button: ButtonConfig) -> None:
    """Draw one configured button and center its label."""
    x, y = button.position
    cv2.rectangle(frame, (x, y), (x + BUTTON_SIZE, y + BUTTON_SIZE), button.color, -1)
    label_size = cv2.getTextSize(button.label, cv2.FONT_HERSHEY_SIMPLEX,
                                 LABEL_FONT_SCALE, FONT_THICKNESS)[0]
    label_position = (x + (BUTTON_SIZE - label_size[0]) // 2,
                      y + (BUTTON_SIZE + label_size[1]) // 2)
    text_color = BLACK if button.color == WHITE else WHITE
    cv2.putText(frame, button.label, label_position, cv2.FONT_HERSHEY_SIMPLEX,
                LABEL_FONT_SCALE, text_color, FONT_THICKNESS)