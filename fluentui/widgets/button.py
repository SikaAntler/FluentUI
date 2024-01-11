from enum import Enum
from typing import Union

from PySide6.QtCore import QEvent, QSize
from PySide6.QtGui import QEnterEvent, QIcon, QMouseEvent, QPixmap
from PySide6.QtWidgets import QPushButton, QToolButton

from ..utils import FluentStyleSheet


class PushButton(QPushButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setIconSize(QSize(16, 16))


class ToolButtonState(Enum):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2


class ToolButton(QToolButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self._icon = QIcon()
        self._text = ""
        self._state = ToolButtonState.NORMAL

        FluentStyleSheet.BUTTON.apply(self)

    def setIcon(self, icon: Union[QIcon, QPixmap]) -> None:
        self._icon = icon
        self.update()

    def icon(self) -> QIcon:
        return self._icon

    def setText(self, text: str) -> None:
        self._text = text

    def text(self) -> str:
        return self._text

    def enterEvent(self, arg__1: QEnterEvent) -> None:
        self._set_state(ToolButtonState.HOVER)
        super().enterEvent(arg__1)

    def leaveEvent(self, arg__1: QEvent) -> None:
        self._set_state(ToolButtonState.NORMAL)
        super().leaveEvent(arg__1)

    def mousePressEvent(self, arg__1: QMouseEvent) -> None:
        self._state = ToolButtonState.PRESSED
        super().mousePressEvent(arg__1)

    def mouseReleaseEvent(self, arg__1: QMouseEvent) -> None:
        self._state = ToolButtonState.NORMAL
        super().mouseReleaseEvent(arg__1)

    def _set_state(self, state: ToolButtonState) -> None:
        self._state = state
        self.update()

    # def paintEvent(self, arg__1: QPaintEvent) -> None:
    #     super().paintEvent(arg__1)
    #
    #     painter = QPainter(self)
    #     painter.setRenderHints(
    #         QPainter.RenderHint.Antialiasing
    #         | QPainter.RenderHint.TextAntialiasing
    #         | QPainter.RenderHint.SmoothPixmapTransform
    #     )
    #
    #     if not self.isEnabled():
    #         painter.setOpacity(0.43)
    #     if self._state == ToolButtonState.PRESSED:
    #         painter.setOpacity(0.63)
    #
    #     w, h = self.iconSize().width(), self.iconSize().height()
    #     x = (self.width() - w) / 2
    #     y = (self.height() - h) / 2
    #     self.icon()
