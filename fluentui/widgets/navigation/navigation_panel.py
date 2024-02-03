from enum import Enum

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    QPropertyAnimation,
    QRect,
    Qt,
)
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ...utils import FIcon, FluentStyleSheet
from .navigation_widget import (
    NavigationSeparator,
    NavigationToolButton,
    NavigationWidget,
)


class PanelPosition(Enum):
    TOP = 0
    SCROLL = 1
    BOTTOM = 2


class PanelState(Enum):
    COLLAPSED = 0
    EXPANDED = 1


class NavigationPanel(QWidget):
    EXPANDED_WIDTH = 312

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self._state = PanelState.COLLAPSED

        # 布局
        self.vlyt = NavigationItemLayout(self)
        self.vlyt_top = NavigationItemLayout()
        self.vlyt_scroll = NavigationItemLayout()
        self.vlyt_bottom = NavigationItemLayout()
        self._init_layout()

        self.btn_menu = NavigationToolButton(FIcon.LINE_HORIZONTAL_3)
        self._init_widgets()

        self.animation = QPropertyAnimation(self, b"geometry", self)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.animation.setDuration(150)

        # signals & slots
        self.btn_menu.clicked.connect(self.toggle)
        self.animation.finished.connect(self.on_animation_finished)

        self.window().installEventFilter(self)

    def _init_layout(self) -> None:
        self.vlyt.setContentsMargins(0, 5, 0, 5)
        self.vlyt.setSpacing(4)
        self.vlyt.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.vlyt_top.setContentsMargins(4, 0, 4, 0)
        self.vlyt_top.setSpacing(4)
        self.vlyt_top.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.vlyt_scroll.setContentsMargins(4, 0, 4, 0)
        self.vlyt_scroll.setSpacing(4)
        self.vlyt_scroll.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.vlyt_scroll.setContentsMargins(4, 0, 4, 0)
        self.vlyt_bottom.setSpacing(4)
        self.vlyt_bottom.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.vlyt.addLayout(self.vlyt_top, 0)
        self.vlyt.addLayout(self.vlyt_scroll, 1)
        self.vlyt.addLayout(self.vlyt_bottom, 0)

        # self.resize(48, self.height())
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        FluentStyleSheet.NAVIGATION.apply(self)

    def _init_widgets(self) -> None:
        self.vlyt_top.addWidget(self.btn_menu)

    def addWidget(self, widget: NavigationWidget, position=PanelPosition.TOP) -> None:
        self.insertWidget(-1, widget, position)

    def insertWidget(
        self, index, widget: NavigationWidget, position=PanelPosition.TOP
    ) -> None:
        widget.setParent(self)
        if position == PanelPosition.TOP:
            self.vlyt_top.insertWidget(index, widget)
        elif position == PanelPosition.SCROLL:
            self.vlyt_scroll.insertWidget(index, widget)
        elif position == PanelPosition.BOTTOM:
            self.vlyt_bottom.insertWidget(index, widget)
        # widget.show()

    def toggle(self) -> None:
        if self._state == PanelState.COLLAPSED:
            self.expand()
        else:
            self.collapse()

    def expand(self) -> None:
        if self.animation.state() == QPropertyAnimation.State.Running:
            return

        self._set_widgets_expanded(True)

        self.show()

        self.animation.setStartValue(QRect(self.x(), self.y(), 48, self.height()))
        self.animation.setEndValue(
            QRect(self.x(), self.y(), self.EXPANDED_WIDTH, self.height())
        )
        self.animation.start()

        self._state = PanelState.EXPANDED
        # self.animation.setProperty("expand", True)

    def collapse(self) -> None:
        if self.animation.state() == QPropertyAnimation.State.Running:
            return

        self._set_widgets_expanded(False)

        self.animation.setStartValue(
            QRect(self.x(), self.y(), self.EXPANDED_WIDTH, self.height())
        )
        self.animation.setEndValue(QRect(self.x(), self.y(), 48, self.height()))
        self.animation.start()

        self._state = PanelState.COLLAPSED
        # self.animation.setProperty("expand", False)

    def on_animation_finished(self):
        # if not self.animation.property("expand"):
        if self._state == PanelState.COLLAPSED:
            self.hide()

    def setMenuButtonVisible(self, is_visible: bool) -> None:
        self.btn_menu.setVisible(is_visible)

    def _set_widgets_expanded(self, is_expanded: bool) -> None:
        for widget in self.findChildren(NavigationWidget):
            widget.setExpanded(is_expanded)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.MouseButtonRelease:
            if not self.geometry().contains(event.pos()):
                self.collapse()

        if event.type() == QEvent.Type.Resize:
            self.setFixedHeight(event.size().height() - 31)

        return super().eventFilter(watched, event)


class NavigationItemLayout(QVBoxLayout):
    def setGeometry(self, rect: QRect) -> None:
        super().setGeometry(rect)

        for i in range(self.count()):
            item = self.itemAt(i)
            if isinstance(item.widget(), NavigationSeparator):
                geometry = item.geometry()
                item.widget().setGeometry(
                    0, geometry.y(), geometry.width(), geometry.height()
                )
