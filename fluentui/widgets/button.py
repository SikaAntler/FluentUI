from PySide6.QtCore import QEvent, QRect, QRectF, QSize
from PySide6.QtGui import (
    QEnterEvent,
    QIcon,
    QMouseEvent,
    QPainter,
    QPaintEvent,
)
from PySide6.QtWidgets import QPushButton, QToolButton

from ..utils import FStyleSheet, Icon, draw_icon, set_font


class FPushButton(QPushButton):
    def __init__(
        self,
        text: str = "",
        parent=None,
        icon: QIcon | Icon = None,
    ) -> None:
        super().__init__(text=text, parent=parent)

        self._icon = icon
        self.setIcon(icon)
        self.setIconSize(QSize(20, 20))

        self._is_hover = False
        self._is_pressed = False

        FStyleSheet.BUTTON.apply(self)
        set_font(self)

    def icon(self) -> QIcon | Icon | None:
        return self._icon

    def setIcon(self, icon: QIcon | Icon) -> None:
        self._icon = icon
        self.setProperty("hasIcon", icon is not None)

    def enterEvent(self, event: QEnterEvent) -> None:
        self._is_hover = True
        super().enterEvent(event)

    def leaveEvent(self, event: QEnterEvent) -> None:
        self._is_hover = False
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = False
        super().mouseReleaseEvent(event)

    def _draw_icon(
        self,
        painter: QPainter,
        rect: QRect | QRectF,
        state: QIcon.State = QIcon.State.Off,
    ) -> None:
        draw_icon(self._icon, painter, rect, state)

    def paintEvent(self, event: QPaintEvent) -> None:
        # TODO: super必须要在绘制icon前，否则icon颜色不正常
        super().paintEvent(event)

        if self._icon is not None:
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
            y = (self.height() - h) / 2
            mw = self.minimumSizeHint().width()
            # TODO: 为什么要判断mw>0，在特殊情况下真实尺寸有可能小于SizeHint？
            x = 12 + (self.width() - mw) / 2 if mw > 0 else 12
            self._draw_icon(painter, QRectF(x, y, w, h))


class PrimaryPushButton(FPushButton):
    def __init__(self, text: str = "", parent=None, icon: Icon = None) -> None:
        super().__init__(text=text, parent=parent, icon=icon)

    def _draw_icon(
        self,
        painter: QPainter,
        rect: QRect | QRectF,
        state: QIcon.State = QIcon.State.Off,
    ) -> None:
        if not self.isEnabled():
            painter.setOpacity(0.9)
        draw_icon(self._icon, painter, rect, QIcon.State.On)


class ToolButton(QToolButton):
    def __init__(self, icon: Icon, text: str, parent=None) -> None:
        super().__init__(parent=parent)

        self._icon = icon
        self.setIconSize(QSize(24, 24))
        self._text = text

        self._is_hover = False
        self._is_pressed = False

        self._post_init()

        FStyleSheet.BUTTON.apply(self)
        set_font(self)

    def icon(self) -> Icon:
        return self._icon

    def setIcon(self, icon: Icon) -> None:
        self._icon = icon
        self.update()

    def text(self) -> str:
        return self._text

    def setText(self, text: str) -> None:
        self._text = text

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
