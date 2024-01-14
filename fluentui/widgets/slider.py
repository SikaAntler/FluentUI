from PySide6.QtCore import (
    Property,
    QEvent,
    QPoint,
    QPointF,
    QPropertyAnimation,
    Qt,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QEnterEvent,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QResizeEvent,
)
from PySide6.QtWidgets import QSlider, QWidget


class SliderHandle(QWidget):
    pressed = Signal()
    released = Signal()

    def __init__(self, parent: QSlider) -> None:
        super().__init__(parent=parent)

        self.setFixedSize(22, 22)
        self._radius = 5

        self._animation = QPropertyAnimation(self, b"radius", self)
        self._animation.setDuration(100)

    def enterEvent(self, event: QEnterEvent) -> None:
        self._start_animation(6)

    def leaveEvent(self, event: QEvent) -> None:
        self._start_animation(5)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._start_animation(4)
        self.pressed.emit()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._start_animation(6)
        self.released.emit()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        # 外圈
        painter.setPen(QColor(0, 0, 0, 25))
        painter.setBrush(QColor("white"))
        painter.drawEllipse(self.rect().adjusted(1, 1, -1, -1))

        # 内圈
        painter.setBrush(QColor(0, 159, 170))
        painter.drawEllipse(QPoint(11, 11), self._radius, self._radius)

    @Property(int)
    def radius(self) -> int:
        return self._radius

    @radius.setter
    def radius(self, r: int) -> None:
        self._radius = r
        self.update()

    def _start_animation(self, radius: int) -> None:
        self._animation.stop()
        self._animation.setStartValue(self._radius)
        self._animation.setEndValue(radius)
        self._animation.start()


class FSlider(QSlider):
    def __init__(self, orientation: Qt.Orientation, parent=None) -> None:
        super().__init__(orientation=orientation, parent=parent)

        self._handle = SliderHandle(self)

        # TODO: 必须设置minimum值，否则会出现只绘制一半的情况
        if orientation == Qt.Orientation.Horizontal:
            self.setMinimumHeight(22)
        else:
            self.setMinimumWidth(22)

        self._handle.pressed.connect(self.sliderPressed)
        self._handle.released.connect(self.sliderReleased)
        self.valueChanged.connect(self._adjust_handle_pos)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.setValue(self._pos_to_value(event.position()))

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.setValue(self._pos_to_value(event.position()))

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 100))

        if self.orientation() == Qt.Orientation.Horizontal:
            w = self.width()
            painter.drawRoundedRect(11, 11 - 2, w - 22, 4, 2, 2)

            painter.setBrush(QColor(0, 159, 170))
            aw = int(
                (self.value() - self.minimum())
                / (self.maximum() - self.minimum())
                * (w - 22)
            )
            painter.drawRoundedRect(11, 11 - 2, aw, 4, 2, 2)
        else:
            h = self.height()
            painter.drawRoundedRect(11 - 2, 11, 4, h - 22, 2, 2)

            painter.setBrush(QColor(0, 159, 170))
            ah = int(
                (self.value() - self.minimum())
                / (self.maximum() - self.minimum())
                * (h - 22)
            )
            painter.drawRoundedRect(11 - 2, h - 11 - ah, 4, ah, 2, 2)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self._adjust_handle_pos()

    def _adjust_handle_pos(self) -> None:
        coff = self._groove_length / (self.maximum() - self.minimum())

        if self.orientation() == Qt.Orientation.Horizontal:
            delta = int((self.value() - self.minimum()) * coff)
            self._handle.move(delta, 0)
        else:
            delta = int((self.maximum() - self.value()) * coff)
            self._handle.move(0, delta)

    @property
    def _groove_length(self) -> int:
        if self.orientation() == Qt.Orientation.Horizontal:
            length = self.width()
        else:
            length = self.height()

        return length - 22

    def _pos_to_value(self, pos: QPointF) -> int:
        coff = (self.maximum() - self.minimum()) / self._groove_length

        if self.orientation() == Qt.Orientation.Horizontal:
            value = int((pos.x() - 11) * coff) + self.minimum()
        else:
            value = self.maximum() - int((pos.y() - 11) * coff)

        return value
