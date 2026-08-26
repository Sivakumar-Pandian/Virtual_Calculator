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


BUTTON_SIZE: Final[int] = 60
PINCH_DISTANCE_THRESHOLD: Final[float] = 30.0
CLICK_DEBOUNCE_SECONDS: Final[float] = 0.3
PINCH_REQUIRED_FRAMES: Final[int] = 2
PINCH_RELEASE_MULTIPLIER: Final[float] = 1.35
FINGERTIP_SMOOTHING: Final[float] = 0.55
INDEX_FINGER_LANDMARK: Final[int] = 8
MIDDLE_FINGER_LANDMARK: Final[int] = 12
DETECTION_CONFIDENCE: Final[float] = 0.5
TRACKING_CONFIDENCE: Final[float] = 0.5
EXPRESSION_POSITION: Final[Position] = (50, 80)
EXPRESSION_FONT_SCALE: Final[float] = 1.5
LABEL_FONT_SCALE: Final[float] = 0.8
FONT_THICKNESS: Final[int] = 2
BLACK: Final[Color] = (0, 0, 0)
WHITE: Final[Color] = (255, 255, 255)
RED: Final[Color] = (0, 0, 255)
OVERLAY_WEIGHT: Final[float] = 0.6
FRAME_WEIGHT: Final[float] = 0.4
EXIT_KEY: Final[int] = 27

BUTTON_CONFIGS: Final[tuple[ButtonConfig, ...]] = (
    ButtonConfig("7", (50, 100), WHITE),
    ButtonConfig("8", (110, 100), WHITE),
    ButtonConfig("9", (170, 100), WHITE),
    ButtonConfig("/", (230, 100), WHITE),
    ButtonConfig("4", (50, 160), WHITE),
    ButtonConfig("5", (110, 160), WHITE),
    ButtonConfig("6", (170, 160), WHITE),
    ButtonConfig("*", (230, 160), WHITE),
    ButtonConfig("1", (50, 220), WHITE),
    ButtonConfig("2", (110, 220), WHITE),
    ButtonConfig("3", (170, 220), WHITE),
    ButtonConfig("-", (230, 220), WHITE),
    ButtonConfig("CLR", (50, 280), RED),
    ButtonConfig("0", (110, 280), WHITE),
    ButtonConfig("=", (170, 280), WHITE),
    ButtonConfig("+", (230, 280), WHITE),
)