from enum import Enum
from typing import Callable

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QObject,
    QPropertyAnimation,
    QRect,
    Qt,
)
from PySide6.QtWidgets import QVBoxLayout, QWidget

from ...utils import FIcon, FStyleSheet
from .navigation_widget import (
    NavigationPushButton,
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
    EXPANDED_WIDTH = 322

    def __init__(self, parent=None, hide: bool = False) -> None:
        super().__init__(parent=parent)

        self._parent = parent
        self._hide = hide
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

        self.vlyt_bottom.setContentsMargins(4, 0, 4, 0)
        self.vlyt_bottom.setSpacing(4)
        self.vlyt_bottom.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.vlyt.addLayout(self.vlyt_top, 0)
        self.vlyt.addLayout(self.vlyt_scroll, 1)
        self.vlyt.addLayout(self.vlyt_bottom, 0)

        # self.resize(48, self.height())
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setProperty("expand", False)
        FStyleSheet.NAVIGATION.apply(self)

    def _init_widgets(self) -> None:
        self.vlyt_top.addWidget(self.btn_menu)

    def addWidget(
        self,
        widget: NavigationWidget,
        on_clicked: Callable = None,
        position: PanelPosition = PanelPosition.TOP,
    ) -> None:
        self.insertWidget(-1, widget, on_clicked, position)

    def insertWidget(
        self,
        index: int,
        widget: NavigationWidget,
        on_clicked: Callable = None,
        position: PanelPosition = PanelPosition.TOP,
    ) -> None:
        widget.setParent(self)

        if hasattr(widget, "text"):
            widget.setObjectName(widget.text())
        widget.clicked.connect(self.on_widget_clicked)

        if on_clicked is not None:
            widget.clicked.connect(on_clicked)

        if position == PanelPosition.TOP:
            self.vlyt_top.insertWidget(index, widget)
        elif position == PanelPosition.SCROLL:
            self.vlyt_scroll.insertWidget(index, widget)
        elif position == PanelPosition.BOTTOM:
            self.vlyt_bottom.insertWidget(index, widget)

    def addItem(
        self,
        icon: FIcon,
        text: str,
        on_clicked: Callable = None,
        position: PanelPosition = PanelPosition.TOP,
    ) -> None:
        self.insertItem(-1, icon, text, on_clicked, position)

    def insertItem(
        self,
        index: int,
        icon,
        text: str,
        on_clicked: Callable = None,
        position: PanelPosition = PanelPosition.TOP,
    ) -> None:
        widget = NavigationPushButton(icon, text)
        self.insertWidget(index, widget, on_clicked, position)

    def addSeperator(self, position: PanelPosition = PanelPosition.TOP) -> None:
        self.insertSeperator(-1, position)

    def insertSeperator(
        self, index: int, position: PanelPosition = PanelPosition.TOP
    ) -> None:
        seperator = NavigationSeparator(self)
        self.insertWidget(index, seperator, None, position)

    def toggle(self) -> None:
        if self._state == PanelState.COLLAPSED:
            self.expand()
        else:
            self.collapse()

    def expand(self) -> None:
        if self.animation.state() == QPropertyAnimation.State.Running:
            return

        self._set_widgets_expanded(True)

        self.setProperty("expand", True)
        self.setStyleSheet(self.styleSheet())

        # panel的父类必须设置为窗口，否则会被其他控件覆盖
        if not self.parent().isWindow():
            pos = self.parent().pos()
            pos = self.mapTo(self.window(), pos)
            self.setParent(self.window())
            self.move(pos)
            self.show()

        self.animation.setStartValue(QRect(self.x(), self.y(), 48, self.height()))
        self.animation.setEndValue(
            QRect(self.x(), self.y(), self.EXPANDED_WIDTH, self.height())
        )
        self.animation.start()

        self._state = PanelState.EXPANDED

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

    def on_animation_finished(self):
        if self._state == PanelState.COLLAPSED:
            self.setProperty("expand", False)
            self.setStyleSheet(self.styleSheet())

            if self._hide:
                self.hide()

    def setMenuButtonVisible(self, is_visible: bool) -> None:
        self.btn_menu.setVisible(is_visible)

    def _set_widgets_expanded(self, is_expanded: bool) -> None:
        for widget in self.findChildren(NavigationWidget):
            widget.setExpanded(is_expanded)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if (
            event.type() == QEvent.Type.MouseButtonRelease
            and self._state == PanelState.EXPANDED
        ):
            if not self.geometry().contains(event.pos()):
                self.collapse()

        # if event.type() == QEvent.Type.Resize:
        # self.setFixedHeight(event.size().height() - 31)
        # 此处不能使用event.size()获取大小，返回值为1920*1080，未扣除底部菜单栏的高度

        return super().eventFilter(watched, event)

    def setCurrentItem(self, name: str) -> None:
        for widget in self.findChildren(NavigationPushButton):
            widget.setSelected(widget.text() == name)

    def on_widget_clicked(self) -> None:
        widget = self.sender()
        self.setCurrentItem(widget.objectName())

        # 点击后自动折叠
        if self._state == PanelState.EXPANDED:
            self.collapse()


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
