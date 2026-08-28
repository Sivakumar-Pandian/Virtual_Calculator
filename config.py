"""Application configuration for the gesture-controlled calculator."""

from dataclasses import dataclass

Color = tuple[int, int, int]
Position = tuple[int, int]


@dataclass(frozen=True)
class ButtonConfig:
    """Stores the display properties of one calculator button."""

    label: str
    position: Position
    color: Color


BUTTON_SIZE: int = 58
PINCH_DISTANCE_THRESHOLD: float = 30.0
CLICK_DEBOUNCE_SECONDS: float = 0.3
PINCH_REQUIRED_FRAMES: int = 2
PINCH_RELEASE_MULTIPLIER: float = 1.35
FINGERTIP_SMOOTHING: float = 0.55
INDEX_FINGER_LANDMARK: int = 8
MIDDLE_FINGER_LANDMARK: int = 12
DETECTION_CONFIDENCE: float = 0.5
TRACKING_CONFIDENCE: float = 0.5
EXPRESSION_POSITION: Position = (55, 83)
EXPRESSION_FONT_SCALE: float = 1.15
LABEL_FONT_SCALE: float = 0.72
FONT_THICKNESS: int = 2
BLACK: Color = (0, 0, 0)
WHITE: Color = (255, 255, 255)
RED: Color = (0, 0, 255)
BUTTON_CONFIGS: tuple[ButtonConfig, ...] = (
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