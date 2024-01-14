from enum import Enum

from PySide6.QtGui import QColor


class ThemeColor(Enum):
    PRIMARY = "primary"
    LIGHT_1 = "light_1"
    LIGHT_2 = "light_2"
    LIGHT_3 = "light_3"

    def color(self):
        color = QColor(0, 159, 170)

        h, s, v, _ = color.getHsvF()

        if self == self.LIGHT_1:
            v *= 1.05
        elif self == self.LIGHT_2:
            s *= 0.75
            v *= 1.05
        elif self == self.LIGHT_3:
            s *= 0.65
            v *= 1.05

        return QColor.fromHsvF(h, min(s, 1), min(v, 1))
