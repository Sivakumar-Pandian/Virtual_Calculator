"""Application configuration for the gesture-controlled calculator."""

from dataclasses import dataclass
from typing import Final

Color = tuple[int, int, int]
Position = tuple[int, int]


@dataclass(frozen=True)
class ButtonConfig:
    """Stores the display properties of one calculator button."""

    label: str
    position: Position
    color: Color


BUTTON_SIZE: Final[int] = 58
PINCH_DISTANCE_THRESHOLD: Final[float] = 30.0
CLICK_DEBOUNCE_SECONDS: Final[float] = 0.3
PINCH_REQUIRED_FRAMES: Final[int] = 2
PINCH_RELEASE_MULTIPLIER: Final[float] = 1.35
FINGERTIP_SMOOTHING: Final[float] = 0.55
INDEX_FINGER_LANDMARK: Final[int] = 8
MIDDLE_FINGER_LANDMARK: Final[int] = 12
DETECTION_CONFIDENCE: Final[float] = 0.5
TRACKING_CONFIDENCE: Final[float] = 0.5
EXPRESSION_POSITION: Final[Position] = (55, 83)
EXPRESSION_FONT_SCALE: Final[float] = 1.15
LABEL_FONT_SCALE: Final[float] = 0.72
FONT_THICKNESS: Final[int] = 2
BLACK: Final[Color] = (0, 0, 0)
WHITE: Final[Color] = (255, 255, 255)
RED: Final[Color] = (0, 0, 255)
OVERLAY_WEIGHT: Final[float] = 0.6
FRAME_WEIGHT: Final[float] = 0.4
EXIT_KEY: Final[int] = 27

BUTTON_CONFIGS: Final[tuple[ButtonConfig, ...]] = (
    ButtonConfig("7", (48, 112), WHITE),
    ButtonConfig("8", (113, 112), WHITE),
    ButtonConfig("9", (178, 112), WHITE),
    ButtonConfig("/", (243, 112), (80, 190, 170)),
    ButtonConfig("4", (48, 177), WHITE),
    ButtonConfig("5", (113, 177), WHITE),
    ButtonConfig("6", (178, 177), WHITE),
    ButtonConfig("*", (243, 177), (80, 190, 170)),
    ButtonConfig("1", (48, 242), WHITE),
    ButtonConfig("2", (113, 242), WHITE),
    ButtonConfig("3", (178, 242), WHITE),
    ButtonConfig("-", (243, 242), (80, 190, 170)),
    ButtonConfig("CLR", (48, 307), RED),
    ButtonConfig("0", (113, 307), WHITE),
    ButtonConfig("=", (178, 307), (80, 190, 170)),
    ButtonConfig("+", (243, 307), (80, 190, 170)),
)