from enum import Enum

from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import (
    QColor,
    QEnterEvent,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
)
from PySide6.QtWidgets import QAbstractButton


class TitleBarButtonState(Enum):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2


class TitleBarButton(QAbstractButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setFixedSize(46, 32)

        self._state = TitleBarButtonState.NORMAL

        # background color
        self._normal_bg_color = QColor(0, 0, 0, 0)
        self._hover_bg_color = QColor(0, 0, 0, 26)
        self._pressed_bg_color = QColor(0, 0, 0, 51)

        # icon color
        self._normal_color = QColor(0, 0, 0)
        self._hover_color = QColor(0, 0, 0)
        self._pressed_color = QColor(0, 0, 0)

    def enterEvent(self, event: QEnterEvent) -> None:
        self._set_state(TitleBarButtonState.HOVER)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self._set_state(TitleBarButtonState.NORMAL)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._set_state(TitleBarButtonState.PRESSED)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._set_state(TitleBarButtonState.NORMAL)
        super().mouseReleaseEvent(event)

    def isPressed(self) -> bool:
        return self._state == TitleBarButtonState.PRESSED

    def _get_color(self) -> tuple[QColor, QColor]:
        if self._state == TitleBarButtonState.NORMAL:
            return self._normal_color, self._normal_bg_color
        elif self._state == TitleBarButtonState.HOVER:
            return self._hover_color, self._hover_bg_color
        elif self._state == TitleBarButtonState.PRESSED:
            return self._pressed_color, self._pressed_bg_color

    def _set_state(self, state: TitleBarButtonState) -> None:
        self._state = state
        self.update()


class MinimizeButton(TitleBarButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        # self.painter = QPainter(self)
        # 不能在__init__中生效painter，必须要在paintEvent里定义，否则无效

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        color, bg_color = self._get_color()

        # draw background
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(color, 1)
        # 源代码是设置了Cosmetic，但在4K屏上看太细了，实际看起来颜色很淡
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self._is_max = False

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        color, bg_color = self._get_color()

        # draw background
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(color, 1)
        painter.setPen(pen)

        if not self._is_max:
            painter.drawRect(18, 11, 10, 10)
        else:
            painter.drawRect(18, 13, 8, 8)
            x0, y0, dw = 18 + 2, 13, 2
            path = QPainterPath(QPoint(x0, y0))
            path.lineTo(x0, y0 - dw)
            path.lineTo(x0 + 8, y0 - dw)
            path.lineTo(x0 + 8, y0 - dw + 8)
            path.lineTo(x0 + 8 - dw, y0 - dw + 8)
            painter.drawPath(path)

    def set_max_state(self, is_max: bool) -> None:
        if self._is_max == is_max:
            return

        self._is_max = is_max
        self._set_state(TitleBarButtonState.NORMAL)


class CloseButton(TitleBarButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self._hover_bg_color = QColor(232, 17, 35)
        self._pressed_bg_color = QColor(241, 112, 122)

        self._hover_color = QColor("white")
        self._pressed_color = QColor("white")

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)
        color, bg_color = self._get_color()

        # draw background
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # draw icon
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(color, 1)
        painter.setPen(pen)
        painter.drawLine(18, 11, 28, 21)
        painter.drawLine(18, 21, 28, 11)
