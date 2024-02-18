import math

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    Qt,
)
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import QProgressBar, QLabel

from ..utils import ThemeColor


class FProgressBar(QProgressBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setFixedHeight(4)
        self._background = QColor(0, 0, 0, 155)

        self._val = 0
        self.animation = QPropertyAnimation(self, b"val", self)
        self.animation.setDuration(150)

        self._bar_color = ThemeColor.PRIMARY.color()
        self._is_paused = False
        self._is_error = False

        self.valueChanged.connect(self._on_valueChanged)
        self.setValue(self._val)

    @Property(int)
    def val(self) -> int:
        return self._val

    @val.setter
    def val(self, val: int) -> None:
        self._val = val
        self.update()

    def pause(self) -> None:
        self._is_paused = True
        self.update()

    def isPaused(self) -> bool:
        return self._is_paused

    def resume(self) -> None:
        self._is_paused = False
        self._is_error = False
        self.update()

    def error(self) -> None:
        self._is_error = True
        self.update()

    def isError(self) -> bool:
        return self._is_error

    def barColor(self) -> QColor:
        return self._bar_color

    def setBarColor(self, color: QColor) -> None:
        self._bar_color = color

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        painter.setPen(self._background)
        y = math.floor(self.height() / 2)
        painter.drawLine(0, y, self.width(), y)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._get_bar_color())
        w = int(self._val / (self.maximum() - self.minimum()) * self.width())
        r = self.height() / 2
        painter.drawRoundedRect(0, 0, w, self.height(), r, r)

    def _get_bar_color(self) -> QColor:
        if self._is_paused:
            return QColor(157, 93, 0)
        elif self._is_error:
            return QColor(196, 43, 28)
        else:
            return self._bar_color

    def _on_valueChanged(self, value) -> None:
        self.animation.stop()
        self.animation.setEndValue(value)
        self.animation.start()
        super().setValue(value)


class IndeterminateProgressBar(QProgressBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setFixedHeight(4)
        self._bar_color = ThemeColor.PRIMARY.color()

        self._short_pos = 0
        self.animation_short = QPropertyAnimation(self, b"shortPos", self)

        self._long_pos = 0
        self.animation_long = QPropertyAnimation(self, b"longPos", self)

        self._is_error = False

        self.group_animations = QParallelAnimationGroup(self)
        self.group_long_ani = QSequentialAnimationGroup(self)

        self.animation_short.setDuration(833)
        self.animation_short.setStartValue(0)
        self.animation_short.setEndValue(1.45)

        self.animation_long.setDuration(1167)
        self.animation_long.setStartValue(0)
        self.animation_long.setEndValue(1.75)
        self.animation_long.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.group_animations.addAnimation(self.animation_short)
        self.group_long_ani.addPause(785)
        self.group_long_ani.addAnimation(self.animation_long)
        self.group_animations.addAnimation(self.group_long_ani)
        self.group_animations.setLoopCount(-1)

    @Property(float)
    def shortPos(self) -> int:
        return self._short_pos

    @shortPos.setter
    def shortPos(self, pos: int) -> None:
        self._short_pos = pos
        self.update()

    @Property(float)
    def longPos(self) -> int:
        return self._long_pos

    @longPos.setter
    def longPos(self, pos: int) -> None:
        self._long_pos = pos
        self.update()

    def start(self) -> None:
        self._short_pos = 0
        self._long_pos = 0
        self.group_animations.start()
        self.update()

    def stop(self):
        self.group_animations.stop()
        self._short_pos = 0
        self._long_pos = 0
        self.update()

    def pause(self) -> None:
        self.group_animations.pause()
        self.update()

    def isPaused(self) -> bool:
        return self.group_animations.state() == QParallelAnimationGroup.State.Paused

    def resume(self) -> None:
        self.group_animations.resume()
        self.update()

    def error(self) -> None:
        self._is_error = False
        self.update()

    def isError(self) -> bool:
        return self._is_error

    def barColor(self) -> QColor:
        return self._bar_color

    def setBarColor(self, color: QColor) -> None:
        self._bar_color = color

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._get_bar_color())

        r = self.height() / 2

        x = int((self._short_pos - 0.4) * self.width())
        w = int(0.4 * self.width())
        painter.drawRoundedRect(x, 0, w, self.height(), r, r)

        x = int((self._long_pos - 0.6) * self.width())
        w = int(0.6 * self.width())
        painter.drawRoundedRect(x, 0, w, self.height(), r, r)

    def _get_bar_color(self) -> QColor:
        if self.isPaused():
            return QColor(157, 93, 0)
        elif self._is_error:
            return QColor(196, 43, 28)
        else:
            return self._bar_color
