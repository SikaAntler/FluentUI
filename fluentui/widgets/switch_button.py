from enum import Enum

from PySide6.QtCore import Property, QEvent, QPropertyAnimation, Qt
from PySide6.QtGui import (
    QColor,
    QEnterEvent,
    QMouseEvent,
    QPainter,
    QPaintEvent,
)
from PySide6.QtWidgets import QHBoxLayout, QLabel, QToolButton, QWidget

from ..utils import ThemeColor, set_font


class Indicator(QToolButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setCheckable(True)
        self.setFixedSize(42, 22)

        self._is_pressed = False
        self._is_hover = False

        self._slider_x = 5
        self._animation = QPropertyAnimation(self, b"slider_x", self)
        self._animation.setDuration(120)

        self.toggled.connect(self._toggle_slider)

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

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        # 外框
        painter.setPen(self._border_color())
        painter.setBrush(self._background_color())
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 11, 11)

        # 内圆
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._slider_color())
        painter.drawEllipse(self._slider_x, 5, 12, 12)

    @Property(int)
    def slider_x(self) -> int:
        return self._slider_x

    @slider_x.setter
    def slider_x(self, x) -> None:
        self._slider_x = max(x, 5)
        self.update()

    def toggle(self) -> None:
        self.setChecked(not self.isChecked())

    def _background_color(self) -> QColor:
        if self.isChecked():
            if not self.isEnabled():
                return QColor(0, 0, 0, 56)

            if self._is_pressed:
                return ThemeColor.LIGHT_2.color()
            elif self._is_hover:
                return ThemeColor.LIGHT_1.color()

            return ThemeColor.PRIMARY.color()
        else:
            if not self.isEnabled():
                return QColor(0, 0, 0, 0)

            if self._is_pressed:
                return QColor(0, 0, 0, 23)
            elif self._is_hover:
                return QColor(0, 0, 0, 15)

            return QColor(0, 0, 0, 0)

    def _border_color(self) -> QColor:
        if self.isChecked():
            if self.isEnabled():
                return self._background_color()
            else:
                return QColor(0, 0, 0, 0)
        else:
            if self.isEnabled():
                return QColor(0, 0, 0, 133)

            return QColor(0, 0, 0, 56)

    def _slider_color(self) -> QColor:
        if self.isChecked():
            return QColor("white")
        else:
            if self.isEnabled():
                return QColor(0, 0, 0, 156)
            else:
                return QColor(0, 0, 0, 91)

    def _toggle_slider(self) -> None:
        self._animation.setEndValue(25 if self.isChecked() else 5)
        self._animation.start()


class IndicatorPosition(Enum):
    CENTER = 0
    LEFT = 1
    RIGHT = 2


class FSwitchButton(QWidget):
    def __init__(
        self,
        indicator_pos: IndicatorPosition = IndicatorPosition.CENTER,
        parent=None,
    ) -> None:
        super().__init__(parent=parent)

        self._indicator_pos = indicator_pos
        self._indicator = Indicator(self)

        self._text_off = "关"
        self._text_on = "开"
        self._label = QLabel(self._text_off)

        if indicator_pos != IndicatorPosition.CENTER:
            self.hlyt = QHBoxLayout(self)
            self.hlyt.setContentsMargins(0, 0, 0, 0)
            self.hlyt.setSpacing(12)
            if indicator_pos == IndicatorPosition.LEFT:
                self.hlyt.addWidget(self._indicator, 0)
                self.hlyt.addWidget(self._label, 0)
                self.hlyt.setAlignment(Qt.AlignmentFlag.AlignLeft)
            else:
                self.hlyt.addWidget(self._indicator, 0)
                self.hlyt.addWidget(self._label, 0)
                self.hlyt.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setFixedHeight(22)
        set_font(self, font_size=12)

        self._indicator.toggled.connect(self._switch_text)

    def isChecked(self):
        return self._indicator.isChecked()

    def setChecked(self, isChecked: bool):
        if self._indicator_pos != IndicatorPosition.CENTER:
            self._switch_text()
        self._indicator.setChecked(isChecked)

    def _switch_text(self):
        self._label.setText(self._text_on if self.isChecked() else self._text_off)
        self.adjustSize()
