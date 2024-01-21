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
