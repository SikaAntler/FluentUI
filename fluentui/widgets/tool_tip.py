from enum import Enum

from PySide6.QtCore import (
    QEvent,
    QObject,
    QPoint,
    QPropertyAnimation,
    Qt,
    QTimer,
)
from PySide6.QtGui import QColor, QHideEvent, QShowEvent
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QWidget,
)

from fluentui.utils import FStyleSheet, get_screen_geometry, set_font


class ToolTipPosition(Enum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT_TOP = 4
    RIGHT_TOP = 5
    RIGHT_BOTTOM = 6
    LEFT_BOTTOM = 7


class FToolTip(QWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)

        self._text = text
        self._duration = 1000

        self.hlyt = QHBoxLayout(self)
        self.hlyt.setContentsMargins(12, 8, 12, 12)

        self.container = QFrame(self)
        self.container.setObjectName("container")
        self.hlyt.addWidget(self.container)

        self.hlyt_container = QHBoxLayout(self.container)
        self.hlyt_container.setContentsMargins(8, 6, 8, 8)

        self.label = QLabel(text, self)
        self.label.setObjectName("label")
        self.hlyt_container.addWidget(self.label)
        set_font(self.label, font_size=10)

        self.animation = QPropertyAnimation(self, b"windowOpacity", self)
        self.animation.setDuration(150)

        self.shadow_effect = QGraphicsDropShadowEffect(self)
        self.shadow_effect.setBlurRadius(25)
        self.shadow_effect.setColor(QColor(0, 0, 0, 60))
        self.shadow_effect.setOffset(0, 5)
        self.container.setGraphicsEffect(self.shadow_effect)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)

        self.installEventFilter(self)

        FStyleSheet.TOOL_TIP.apply(self)

    def text(self) -> str:
        return self._text

    def setText(self, text: str) -> None:
        self._text = text
        self.label.setText(text)
        self.container.adjustSize()
        self.adjustSize()

    def duration(self) -> int:
        return self._duration

    def setDuration(self, duration: int) -> None:
        self._duration = duration

    def showEvent(self, event: QShowEvent) -> None:
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

        self.timer.stop()
        if self.duration() > 0:
            self.timer.start(self._duration + self.animation.duration())

        super().showEvent(event)

    def hideEvent(self, event: QHideEvent) -> None:
        self.timer.stop()
        super().hideEvent(event)

    def adjust_pos(self, parent: QWidget, position: ToolTipPosition) -> None:
        manager = ToolTipPositionManager.make(position)
        self.move(manager.position(self, parent))


class ToolTipPositionManager:
    managers = {}

    def position(self, tool_tip: FToolTip, parent: QWidget) -> QPoint:
        pos = self._position(tool_tip, parent)
        rect = get_screen_geometry()
        x = max(rect.left(), min(pos.x(), rect.right() - tool_tip.width() - 4))
        y = max(rect.top(), min(pos.y(), rect.bottom() - tool_tip.height() - 4))

        return QPoint(x, y)

    def _position(self, tool_tip: FToolTip, parent: QWidget) -> QPoint:
        raise NotImplementedError

    @classmethod
    def register(cls, name: ToolTipPosition):
        def wrapper(manager):
            if name not in cls.managers:
                cls.managers[name] = manager

            return manager

        return wrapper

    @classmethod
    def make(cls, position: ToolTipPosition) -> "ToolTipPositionManager":
        if position not in cls.managers:
            raise ValueError(f"`{position}` is an invalid tool tip position")

        return cls.managers[position]()


@ToolTipPositionManager.register(ToolTipPosition.LEFT)
class ToolTipPositionLeft(ToolTipPositionManager):
    def _position(self, tool_tip: FToolTip, parent: QWidget) -> QPoint:
        x = -tool_tip.width()
        y = (parent.height() - tool_tip.height()) // 2 + 2  # +2是为了抵消阴影的offset

        return parent.mapToGlobal(QPoint(x, y))


@ToolTipPositionManager.register(ToolTipPosition.TOP)
class ToolTipPositionTop(ToolTipPositionManager):
    def _position(self, tool_tip: FToolTip, parent: QWidget) -> QPoint:
        x = (parent.width() - tool_tip.width()) // 2
        y = -tool_tip.height()

        return parent.mapToGlobal(QPoint(x, y))


@ToolTipPositionManager.register(ToolTipPosition.RIGHT)
class ToolTipPositionRight(ToolTipPositionManager):
    def _position(self, tool_tip: FToolTip, parent: QWidget) -> QPoint:
        x = parent.width()
        y = (parent.height() - tool_tip.height()) // 2 + 2

        return parent.mapToGlobal(QPoint(x, y))


@ToolTipPositionManager.register(ToolTipPosition.BOTTOM)
class ToolTipPositionBottom(ToolTipPositionManager):
    def _position(self, tool_tip: FToolTip, parent: QWidget) -> QPoint:
        x = (parent.width() - tool_tip.width()) // 2
        y = parent.height()

        return parent.mapToGlobal(QPoint(x, y))


class FToolTipFilter(QObject):
    def __init__(self, parent=None, delay=300, position=ToolTipPosition.BOTTOM):
        super().__init__(parent=parent)

        self._delay = delay
        self._position = position

        self._tool_tip = None

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._show_tool_tip)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.ToolTip:
            # 存在ToolTip时移动鼠标会反复触发
            return True

        elif event.type() in [QEvent.Type.Hide, QEvent.Type.Leave]:
            self._hide_tool_tip()
        elif event.type() == QEvent.Type.Enter:
            parent: QWidget = self.parent()
            if self._tool_tip is None:
                self._tool_tip = FToolTip(parent.toolTip(), parent)
            self._tool_tip.setDuration(parent.toolTipDuration())
            self.timer.start(self._delay)
        elif event.type() == QEvent.Type.MouseButtonPress:
            self._hide_tool_tip()

        return super().eventFilter(watched, event)

    def _show_tool_tip(self) -> None:
        self._tool_tip.show()  # show要放前面，或者手动调用adjustSize
        self._tool_tip.adjust_pos(self.parent(), self._position)

    def _hide_tool_tip(self) -> None:
        self.timer.stop()
        if self._tool_tip is not None:
            # 页面中有多个FToolTip时，有些未触发可能为None
            self._tool_tip.hide()
