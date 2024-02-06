from enum import Enum

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QEvent,
    QObject,
    QPointF,
    QPropertyAnimation,
    QRectF,
    QSize,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import (
    QColor,
    QEnterEvent,
    QMouseEvent,
    QPainter,
    QPaintEvent,
    QResizeEvent,
    QWheelEvent,
)
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..utils import FIcon, draw_icon


class ArrowButton(QToolButton):
    def __init__(self, icon: FIcon, parent=None) -> None:
        super().__init__(parent=parent)

        self.setFixedSize(10, 10)
        self._icon = icon

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        s = 7 if self.isDown() else 8
        x = (self.width() - s) / 2
        draw_icon(self._icon, painter, QRectF(x, x, s, s), fill="#858789")


class ScrollBarGroove(QWidget):
    def __init__(self, orientation: Qt.Orientation, parent=None) -> None:
        super().__init__(parent=parent)

        if orientation == Qt.Orientation.Vertical:
            self.setFixedWidth(12)
            self.lyt = QVBoxLayout(self)
            self.lyt.setContentsMargins(0, 3, 0, 3)
            self.btn_up = ArrowButton(FIcon.CARET_UP_FILLED, self)
            self.lyt.addWidget(self.btn_up, 0, Qt.AlignmentFlag.AlignHCenter)
            self.lyt.addStretch(1)
            self.btn_down = ArrowButton(FIcon.CARET_DOWN_FILLED, self)
            self.lyt.addWidget(self.btn_down, 0, Qt.AlignmentFlag.AlignHCenter)
        else:
            self.setFixedHeight(12)
            self.lyt = QHBoxLayout(self)
            self.lyt.setContentsMargins(3, 0, 3, 0)
            self.btn_up = ArrowButton(FIcon.CARET_LEFT_FILLED, self)
            self.lyt.addWidget(self.btn_up, 0, Qt.AlignmentFlag.AlignVCenter)
            self.lyt.addStretch(1)
            self.btn_down = ArrowButton(FIcon.CARET_RIGHT_FILLED, self)
            self.lyt.addWidget(self.btn_down, 0, Qt.AlignmentFlag.AlignVCenter)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity_effect.setOpacity(0)
        self.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity", self)
        self.animation.setDuration(150)

    def fadeIn(self) -> None:
        self.animation.setEndValue(1)
        self.animation.start()

    def fadeOut(self) -> None:
        self.animation.setEndValue(0)
        self.animation.start()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(252, 252, 252, 217))
        painter.drawRoundedRect(self.rect(), 6, 6)


class ScrollBarHandle(QWidget):
    def __init__(self, orientation: Qt.Orientation, parent=None) -> None:
        super().__init__(parent=parent)

        self._orientation = orientation
        if orientation == Qt.Orientation.Vertical:
            self.setFixedWidth(3)
        else:
            self.setFixedHeight(3)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 114))

        if self._orientation == Qt.Orientation.Vertical:
            r = self.width() / 2
        else:
            r = self.height() / 2
        painter.drawRoundedRect(self.rect(), r, r)


class ScrollBarRegion(Enum):
    GROOVE_UP = 0
    EMPTY_SLIDER_UP = 1
    HANDLE = 2
    EMPTY_SLIDER_DOWN = 3
    GROOVE_DOWN = 4


class FScrollBar(QWidget):
    rangeChanged = Signal(tuple)
    valueChanged = Signal(int)

    def __init__(
        self, orientation: Qt.Orientation, parent: QAbstractScrollArea
    ) -> None:
        super().__init__(parent=parent)

        self.groove = ScrollBarGroove(orientation, self)
        self.handle = ScrollBarHandle(orientation, self)
        self.timer = QTimer(self)

        self._orientation = orientation
        self._single_step = 1
        self._page_step = 50
        self._padding = 14

        self._minimum = 0
        self._maximum = 0
        self._value = 0

        self._is_entered = False
        self._is_expanded = False
        self._is_drag = False
        self._drag_pos = None

        if orientation == Qt.Orientation.Vertical:
            self.setFixedWidth(12)
            self.ori_bar = parent.verticalScrollBar()
            parent.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            self.setFixedHeight(12)
            self.ori_bar = parent.horizontalScrollBar()
            parent.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.groove.btn_up.clicked.connect(self._on_page_up)
        self.groove.btn_down.clicked.connect(self._on_page_down)
        self.groove.animation.valueChanged.connect(
            self._on_groove_animation_valueChanged
        )

        self.ori_bar.rangeChanged.connect(self.setRange)
        self.ori_bar.valueChanged.connect(self.setValue)
        self.valueChanged.connect(self.ori_bar.setValue)

        parent.installEventFilter(self)

        self.setRange(self.ori_bar.minimum(), self.ori_bar.maximum())
        self.setVisible(self._maximum > 0)

    @Property(int, notify=valueChanged)
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        # 两边ScrollBar的valueChanged信号互发
        if value == self._value:
            # print(f"Same value: {value}")
            return

        value = max(self._minimum, min(value, self._maximum))
        self._value = value
        self.valueChanged.emit(value)

        self._adjust_handle_pos()

    def setValue(self, value: int) -> None:
        self.value = value

    def setRange(self, minimum: int, maximum: int) -> None:
        assert (
            maximum >= minimum
        ), f"Maximum value {maximum} should be greeter than or equal to minimum value {minimum}"

        if minimum == self._minimum and maximum == self._maximum:
            return

        self._minimum = minimum
        self._maximum = maximum

        self._adjust_handle_size()
        self._adjust_handle_pos()
        self.setVisible(maximum > 0)

        self.rangeChanged.emit((minimum, maximum))

    def minimum(self) -> int:
        return self._minimum

    def setMinimum(self, minimum: int) -> None:
        self.setRange(minimum, self._maximum)

    def setMaximum(self, maximum: int) -> None:
        self.setRange(self._minimum, maximum)

    def maximum(self) -> int:
        return self._maximum

    def singleStep(self) -> int:
        return self._single_step

    def setSingleStep(self, step: int) -> None:
        if step > 1:
            self._single_step = step

    def pageStep(self) -> int:
        return self._page_step

    def setPageStep(self, step: int) -> None:
        if step > 1:
            self._page_step = step

    def expand(self) -> None:
        if self._is_expanded or not self._is_entered:
            return

        self._is_expanded = True
        self.groove.fadeIn()

    def collapse(self) -> None:
        if not self._is_expanded or self._is_entered:
            return

        self._is_expanded = False
        self.groove.fadeOut()

    def enterEvent(self, event: QEnterEvent) -> None:
        self._is_entered = True
        self.timer.stop()
        self.timer.singleShot(200, self.expand)

    def leaveEvent(self, event: QEvent) -> None:
        self._is_entered = False
        self.timer.stop()
        self.timer.singleShot(200, self.collapse)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched is self.parent() and isinstance(event, QResizeEvent):
            self._update_geometry(watched.size())
            # self._update_geometry(event.size())
            self._adjust_handle_size()
            self._adjust_handle_pos()

        return super().eventFilter(watched, event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        super().mouseMoveEvent(event)

        if not self._is_drag:
            return

        pos = event.position()
        if self._orientation == Qt.Orientation.Vertical:
            delta = pos.y() - self._drag_pos.y()
        else:
            delta = pos.x() - self._drag_pos.x()

        delta = int(
            delta
            / max(self._slider_empty_length(), 1)
            * (self._maximum - self._minimum)
        )
        if delta != 0:
            self.setValue(self._value + delta)

        self._drag_pos = pos

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)

        pos = event.position()
        region = self._get_region(pos)
        if region == ScrollBarRegion.HANDLE:  # 拖拽
            self._is_drag = True
            self._drag_pos = pos
            return

        if region in [
            ScrollBarRegion.GROOVE_UP,
            ScrollBarRegion.GROOVE_DOWN,
        ]:  # 点按钮
            return

        # if self._orientation == Qt.Orientation.Vertical:
        #     if region == ScrollBarRegion.EMPTY_SLIDER_UP:
        #         value = pos.y() - self._padding
        #     else:
        #         value = pos.y() - self.handle.height() - self._padding
        # else:
        #     if region == ScrollBarRegion.EMPTY_SLIDER_UP:
        #         value = pos.x() - self._padding
        #     else:
        #         value = pos.x() - self.handle.width() - self._padding
        # value = int(value / max(self._slider_empty_length(), 1) * self._maximum)

        if self._orientation == Qt.Orientation.Vertical:
            value = pos.y() - self._padding
        else:
            value = pos.x() - self._padding
        value = int(value / max(self._slider_length(), 1) * self._maximum)

        self.setValue(value)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self._is_drag = False
        self._drag_pos = None

    def wheelEvent(self, event: QWheelEvent) -> None:
        super().wheelEvent(event)
        self.parent().wheelEvent(event)

    def _on_page_up(self) -> None:
        self.setValue(self._value - self._page_step)

    def _on_page_down(self) -> None:
        self.setValue(self._value + self._page_step)

    def _on_groove_animation_valueChanged(self) -> None:
        opacity = self.groove.opacity_effect.opacity()
        width = int(3 + opacity * 3)
        if self._orientation == Qt.Orientation.Vertical:
            self.handle.setFixedWidth(width)
        else:
            self.handle.setFixedHeight(width)

        self._adjust_handle_pos()

    def _slider_length(self) -> int:
        if self._orientation == Qt.Orientation.Vertical:
            return self.height() - 2 * self._padding
        else:
            return self.width() - 2 * self._padding

    def _slider_empty_length(self) -> int:
        if self._orientation == Qt.Orientation.Vertical:
            return self._slider_length() - self.handle.height()
        else:
            return self._slider_length() - self.handle.width()

    def _update_geometry(self, size: QSize) -> None:
        if self._orientation == Qt.Orientation.Vertical:
            height = size.height() - 2
            self.setFixedHeight(height)
            self.groove.setFixedHeight(height)
            self.move(size.width() - 13, 1)
        else:
            width = size.width() - 2
            self.setFixedWidth(width)
            self.groove.setFixedWidth(width)
            self.move(1, size.height() - 13)

    def _adjust_handle_size(self) -> None:
        slider_length = self._slider_length()
        handle_length = int(
            slider_length / (1 + (self._maximum - self._minimum) / slider_length)
        )
        if self._orientation == Qt.Orientation.Vertical:
            self.handle.setFixedHeight(max(30, handle_length))
        else:
            self.handle.setFixedWidth(max(30, handle_length))

    def _adjust_handle_pos(self) -> None:
        ratio = self._value / max(self._maximum - self._minimum, 1)
        slider_empty_length = self._slider_empty_length()
        delta = int(ratio * slider_empty_length)

        if self._orientation == Qt.Orientation.Vertical:
            x = self.width() - self.handle.width() - 3
            self.handle.move(x, self._padding + delta)
        else:
            y = self.height() - self.handle.height() - 3
            self.handle.move(self._padding + delta, y)

    def _get_region(self, pos: QPointF) -> ScrollBarRegion:
        if self._orientation == Qt.Orientation.Vertical:
            pos = pos.y()
            length = self.height()
            handle_begin = self.handle.y()
            handle_end = handle_begin + self.handle.height()
        else:
            pos = pos.x()
            length = self.width()
            handle_begin = self.handle.x()
            handle_end = handle_begin + self.handle.width()

        if pos < self._padding:
            return ScrollBarRegion.GROOVE_UP
        elif self._padding <= pos < handle_begin:
            return ScrollBarRegion.EMPTY_SLIDER_UP
        elif handle_begin <= pos <= handle_end:
            return ScrollBarRegion.HANDLE
        elif handle_end < pos <= length - self._padding:
            return ScrollBarRegion.EMPTY_SLIDER_DOWN
        else:
            return ScrollBarRegion.GROOVE_DOWN


class FSmoothScrollBar(FScrollBar):
    def __init__(self, orientation: Qt.Orientation, parent: QAbstractScrollArea):
        super().__init__(orientation, parent)

        self.animation = QPropertyAnimation(self, b"value", self)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._vertical_scroll_rate = 3
        self._vertical_duration = 240
        self._horizontal_scroll_rate = 60
        self._horizontal_duration = 480

        parent.viewport().installEventFilter(self)
        self.installEventFilter(self)

    def scrollByValue(self, dv: int) -> None:
        self.animation.stop()

        if self._orientation == Qt.Orientation.Vertical:
            self.animation.setDuration(self._vertical_duration)
        else:
            self.animation.setDuration(self._horizontal_duration)

        self.animation.setStartValue(self._value)
        self.animation.setEndValue(self._value + dv)
        self.animation.start()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        is_obj = watched is self.parent().viewport() or watched is self
        if is_obj and isinstance(event, QWheelEvent):
            delta = event.angleDelta()
            if self._orientation == Qt.Orientation.Vertical and delta.y() != 0:
                if delta.y() < 0:
                    dv = self._vertical_scroll_rate
                else:
                    dv = -self._vertical_scroll_rate
                self.scrollByValue(dv)
                return True
            elif self._orientation == Qt.Orientation.Horizontal and delta.x() != 0:
                if delta.x() < 0:
                    dv = self._horizontal_scroll_rate
                else:
                    dv = -self._horizontal_scroll_rate
                self.scrollByValue(dv)
                return True

        return super().eventFilter(watched, event)
