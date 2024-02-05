from PySide6.QtCore import QEvent, QRectF, Qt, Signal
from PySide6.QtGui import (
    QColor,
    QEnterEvent,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QPen,
)
from PySide6.QtWidgets import QWidget

from ...utils import FIcon, ThemeColor, draw_icon, set_font


class NavigationWidget(QWidget):
    EXPANDED_WIDTH = 312
    clicked = Signal(bool)
    selectedChanged = Signal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self._is_expanded = False
        self.setFixedSize(40, 36)

        self._is_hover = False
        self._is_pressed = False
        self._is_selected = False

    def enterEvent(self, event: QEnterEvent) -> None:
        self._is_hover = True
        # super().enterEvent(event)  # QWidget默认实现为ignore，因此无效
        self.update()

    def leaveEvent(self, event: QEvent) -> None:
        self._is_hover = False
        self._is_pressed = False
        self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = False
        self.clicked.emit(True)

    def setExpanded(self, is_expanded: bool) -> None:
        if is_expanded == self._is_expanded:
            return

        self._is_expanded = is_expanded
        if is_expanded:
            self.setFixedSize(self.EXPANDED_WIDTH, 36)
        else:
            self.setFixedSize(40, 36)

        self.update()

    def setSelected(self, is_selected: bool) -> None:
        if self._is_selected == is_selected:
            return

        self._is_selected = is_selected
        self.update()
        self.selectedChanged.emit(is_selected)


class NavigationPushButton(NavigationWidget):
    ICON_SIZE = 20

    def __init__(self, icon: FIcon, text: str, parent=None) -> None:
        super().__init__(parent=parent)

        self._icon = icon
        self._text = text

        set_font(self)

    def icon(self) -> FIcon:
        return self._icon

    def setIcon(self, icon: FIcon) -> None:
        self._icon = icon
        self.update()

    def text(self) -> str:
        return self._text

    def setText(self, text: str) -> None:
        self._text = text
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing
        )
        painter.setPen(Qt.PenStyle.NoPen)

        if self._is_pressed:
            painter.setOpacity(0.7)
        if not self.isEnabled():
            painter.setOpacity(0.4)

        if self._is_selected:
            # background
            painter.setBrush(QColor(0, 0, 0, 6 if self._is_hover else 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

            # indicator
            painter.setBrush(ThemeColor.PRIMARY.color())
            painter.drawRoundedRect(0, 10, 3, 16, 1.5, 1.5)
        elif self._is_hover and self.isEnabled():
            painter.setBrush(QColor(0, 0, 0, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # self._icon.paint(painter, 11.5, 10, 16, 16)
        x = (40 - self.ICON_SIZE) / 2 - 0.5
        y = (36 - self.ICON_SIZE) / 2
        draw_icon(self._icon, painter, QRectF(x, y, self.ICON_SIZE, self.ICON_SIZE))

        # text
        if self._is_expanded:
            painter.setFont(self.font())
            painter.setPen(QColor("black"))

            left = 44
            painter.drawText(
                left,
                0,
                self.width() - 13 - left,
                self.height(),
                Qt.AlignmentFlag.AlignVCenter,
                self._text,
            )


class NavigationToolButton(NavigationPushButton):
    def __init__(self, icon: FIcon, parent=None) -> None:
        super().__init__(icon=icon, text="", parent=parent)

    def setExpanded(self, is_expanded: bool) -> None:
        pass


class NavigationSeparator(NavigationWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setExpanded(False)
        self.setFixedSize(48, 3)

    def setExpanded(self, is_expanded: bool) -> None:
        # TODO: 父类子类可共用此函数
        if is_expanded == self._is_expanded:
            return

        self._is_expanded = is_expanded
        if is_expanded:
            self.setFixedSize(self.EXPANDED_WIDTH + 10, 3)
        else:
            self.setFixedSize(48, 3)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0, 15))
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(0, 1, self.width(), 1)
