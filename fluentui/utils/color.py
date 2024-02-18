from enum import Enum

from PySide6.QtGui import QColor


class ThemeColor(Enum):
    PRIMARY = "primary"
    LIGHT_1 = "light_1"
    LIGHT_2 = "light_2"
    LIGHT_3 = "light_3"
    DARK_1 = "dark_1"
    DARK_2 = "dark_2"
    DARK_3 = "dark_3"

    def color(self):
        color = QColor(0, 159, 170)

        h, s, v, _ = color.getHsvF()

        if self == self.LIGHT_1:  # (0, 167, 179)
            v *= 1.05
        elif self == self.LIGHT_2:  # (45, 170, 179)
            s *= 0.75
            v *= 1.05
        elif self == self.LIGHT_3:  # (62, 171, 179)
            s *= 0.65
            v *= 1.05
        elif self == self.DARK_1:  # (0, 119, 128)
            v *= 0.75
        elif self == self.DARK_2:  # (0, 80, 85)
            s *= 1.05
            v *= 0.5
        elif self == self.DARK_3:  # (0, 64, 68)
            s *= 1.1
            v *= 0.4

        return QColor.fromHsvF(h, min(s, 1), min(v, 1))


class FluentColor(Enum):
    YELLOW_GOLD = "#FFB900"
    GOLD = "#FF8C00"
    ORANGE_BRIGHT = "#F7630C"
    ORANGE_DARK = "#CA5010"
    RUST = "#DA3B01"
    PALE_RUST = "#EF6950"
    BRICK_RED = "#D13438"
    MOD_RED = "#FF4343"
    PALE_RED = "#E74856"
    RED = "#E81123"
    ROSE_BRIGHT = "#EA005E"
    ROSE = "#C30052"
    PLUM_LIGHT = "#E3008C"
    PLUM = "#BF0077"
    ORCHID_LIGHT = "#BF0077"
    ORCHID = "#9A0089"
    DEFAULT_BLUE = "#0078D7"
    NAVY_BLUE = "#0063B1"
    PURPLE_SHADOW = "#8E8CD8"
    PURPLE_SHADOW_DARK = "#6B69D6"
    IRIS_PASTEL = "#8764B8"
    IRIS_SPRING = "#744DA9"
    VIOLET_RED_LIGHT = "#B146C2"
    VIOLET_RED = "#881798"
    COOL_BLUE_BRIGHT = "#0099BC"
    COOL_BLUR = "#2D7D9A"
    SEAFOAM = "#00B7C3"
    SEAFOAM_TEAL = "#038387"
    MINT_LIGHT = "#00B294"
    MINT_DARK = "#018574"
    TURF_GREEN = "#00CC6A"
    SPORT_GREEN = "#10893E"
    GRAY = "#7A7574"
    GRAY_BROWN = "#5D5A58"
    STEAL_BLUE = "#68768A"
    METAL_BLUE = "#515C6B"
    PALE_MOSS = "#567C73"
    MOSS = "#486860"
    MEADOW_GREEN = "#498205"
    GREEN = "#107C10"
    OVERCAST = "#767676"
    STORM = "#4C4A48"
    BLUE_GRAY = "#69797E"
    GRAY_DARK = "#4A5459"
    LIDDY_GREEN = "#647C64"
    SAGE = "#525E54"
    CAMOUFLAGE_DESERT = "#847545"
    CAMOUFLAGE = "#7E735F"

    def color(self) -> QColor:
        return QColor(self.value)
