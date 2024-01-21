from typing import Optional

from PySide6.QtCore import QEvent, QRect, QSize, Qt
from PySide6.QtGui import (
    QEnterEvent,
    QIcon,
    QMouseEvent,
    QPainter,
    QPaintEvent,
)
from PySide6.QtWidgets import QPushButton, QToolButton

from ..utils import FluentStyleSheet, set_font, FIcon


class FPushButton(QPushButton):
    def __init__(
        self, icon: Optional[QIcon] = None, text: Optional[str] = None, parent=None
    ) -> None:
        super().__init__(parent=parent)

        self._icon = icon or QIcon()
        self.setIconSize(QSize(20, 20))

        self.setIcon(icon)
        if text is not None:
            self.setText(text)

        self._is_hover = False
        self._is_pressed = False

        set_font(self, font_size=12)
        FluentStyleSheet.BUTTON.apply(self)

    def enterEvent(self, event: QEnterEvent) -> None:
        self._is_hover = True
        super().enterEvent(event)

    def icon(self) -> QIcon:
        return self._icon

    def leaveEvent(self, event: QEnterEvent) -> None:
        self._is_hover = False
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = False
        super().mouseReleaseEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        # TODO: super必须要在绘制icon前，否则icon颜色不正常
        super().paintEvent(event)

        if self._icon:
            painter = QPainter(self)
            painter.setRenderHints(
                QPainter.RenderHint.Antialiasing
                | QPainter.RenderHint.SmoothPixmapTransform,
            )

            if not self.isEnabled():
                painter.setOpacity(0.3628)
            elif self._is_pressed:
                painter.setOpacity(0.786)

            w, h = self.iconSize().toTuple()
            y = (self.height() - h) // 2
            mw = self.minimumSizeHint().width()
            # TODO: 为什么要判断mw>0，在特殊情况下真实尺寸有可能小于SizeHint？
            x = 12 + (self.width() - mw) // 2 if mw > 0 else 12
            self._icon.paint(painter, QRect(x, y, w, h), Qt.AlignmentFlag.AlignCenter)

    def setIcon(self, icon: QIcon) -> None:
        self._icon = icon or QIcon()
        self.setProperty("hasIcon", icon is not None)


class ToolButton(QToolButton):
    def __init__(self, icon: FIcon, text: str, parent=None) -> None:
        super().__init__(parent=parent)

        self._icon = icon
        self.setIconSize(QSize(24, 24))
        self._text = text

        self._is_hover = False
        self._is_pressed = False

        self._post_init()

        set_font(self, font_size=12)
        FluentStyleSheet.BUTTON.apply(self)

    def setIcon(self, icon: FIcon) -> None:
        self._icon = icon
        self.update()

    def icon(self) -> FIcon:
        return self._icon

    def setText(self, text: str) -> None:
        self._text = text

    def text(self) -> str:
        return self._text

    def enterEvent(self, event: QEnterEvent) -> None:
        self._is_hover = True
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self._is_hover = False
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = False
        super().mouseReleaseEvent(event)

    def _post_init(self) -> None:
        pass
