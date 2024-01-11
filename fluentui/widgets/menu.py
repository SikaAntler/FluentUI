from enum import Enum
from typing import Union

from PySide6.QtCore import (
    QEasingCurve,
    QEvent,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    QPoint,
    QPropertyAnimation,
    QSize,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QColor,
    QCursor,
    QHoverEvent,
    QIcon,
    QPainter,
    QPen,
    QPixmap,
    QRegion,
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QWidget,
)

from ..utils import FluentStyleSheet, set_font


class MenuAnimationType(Enum):
    NONE = 0
    DROP_DOWN = 1
    PULL_UP = 2
    FADE_IN_DROP_DOWN = 3
    FADE_IN_DROP_UP = 4


class MenuItemDelegate(QStyledItemDelegate):
    @staticmethod
    def _is_seperator(index: Union[QModelIndex, QPersistentModelIndex]):
        return index.model().data(index, Qt.ItemDataRole.DecorationRole) == "seperator"

    def paint(
            self,
            painter: QPainter,
            option: QStyleOptionViewItem,
            index: Union[QModelIndex, QPersistentModelIndex],
    ) -> None:
        if not self._is_seperator(index):
            return super().paint(painter, option, index)

        painter.save()

        pen = QPen(QColor(0, 0, 0, 25), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        rect = option.rect
        painter.drawLine(0, rect.y() + 4, rect.width() + 12, rect.y() + 4)

        painter.restore()


class MenuActionListWidget(QListWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

        self.setViewportMargins(0, 6, 0, 6)

        # 否则会有...出现
        self.setTextElideMode(Qt.TextElideMode.ElideNone)

        # 原代码是14，但MS只提供有12和16的，我觉得应该根据实际情况来
        self.setIconSize(QSize(16, 16))

        # 丝滑滚动
        self.setVerticalScrollMode(self.ScrollMode.ScrollPerPixel)

        # 否则会出现滚动条，但即使设置Off依然可以滚动
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 自定义委托
        self.setItemDelegate(MenuItemDelegate(self))

        set_font(self)

    def addItem(self, item: QListWidgetItem) -> None:
        super().addItem(item)
        self.adjustSize()

    def adjustSize(self) -> None:
        size = QSize(0, 0)  # QSize() = QSize(-1, -1)
        for i in range(self.count()):
            s = self.item(i).sizeHint()
            size.setWidth(max(size.width(), s.width()))
            size.setHeight(size.height() + s.height())

        # self.viewport().adjustSize()

        margins = self.viewportMargins()
        size += QSize(
            margins.left() + margins.right() + 2, margins.top() + margins.bottom()
        )
        self.setFixedSize(size)


class FMenu(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        # Popup是弹出式
        # FramelessWindowHint无边框，这里不需要titlebar了
        # NoDropShadowWindowHint猜想是因为Win11自带阴影，防止和自己写的冲突
        self.setWindowFlags(
            Qt.WindowType.Popup
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint
        )

        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.view = MenuActionListWidget(self)

        self.menu_layout = QHBoxLayout(self)
        self.menu_layout.addWidget(self.view, 1, Qt.AlignmentFlag.AlignCenter)

        # 决定了内部内容与鼠标之间的距离，原代码设置的很大，应该是为了动画
        # P.S. self.contentsMargin与self.layout().contentsMargins是不同的
        self.menu_layout.setContentsMargins(12, 8, 12, 20)
        # self.menu_layout.setContentsMargins(0, 0, 0, 0)

        # 背景透明, 即使margins设置全0，因为圆角的缘故也会有背景色
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._actions = []  # type: list[QAction]

        self._item_height = 28

        self.view.itemClicked.connect(self._on_item_clicked)

        self.ani_manager = None

        FluentStyleSheet.MENU.apply(self)

        # TODO: 增加对shortcut的支持，至少需要写：
        #  1. ShortcutMenuItemDelegate
        #  2. self._longest_shortcut_width函数

        # TODO: 增加SubMenu功能，需要写的比较多

        # TODO: 原代码对于是否要加icon的逻辑有问题，比如第一个没加，第二个相加怎么办

        # TODO: 增加菜单的弹出动画

        # TODO: 对面对于view、viewport和margins的概念比较迷糊，比如在代码中有如下情况，
        #  self.view.viewportMargins()=(0, 6, 0, 6) 这是初始化时设置的
        #  self.view.contentsMargins()=(1, 1, 1, 1) 这个又影响什么就不清楚了

    def addAction(self, action: QAction) -> None:
        item = self._create_action_item(action)
        self.view.addItem(item)
        self.adjustSize()

    def addSeparator(self) -> None:
        margins = self.view.viewportMargins()
        width = self.view.width() - margins.left() - margins.right()

        item = QListWidgetItem(self.view)
        item.setFlags(Qt.ItemFlag.NoItemFlags)  # 加了就不可以被选中了
        item.setSizeHint(QSize(width, 9))
        self.view.addItem(item)
        item.setData(Qt.ItemDataRole.DecorationRole, "seperator")
        self.adjustSize()

    def adjustSize(self) -> None:
        margins = self.layout().contentsMargins()
        width = self.view.width() + margins.left() + margins.right()
        height = self.view.height() + margins.top() + margins.bottom()
        self.setFixedSize(width, height)

    def _create_action_item(self, action: QAction) -> QListWidgetItem:
        self._actions.append(action)

        icon = self._create_item_icon(action)
        item = QListWidgetItem(icon, action.text())

        self._adjust_item_text(item, action)

        item.setData(Qt.ItemDataRole.UserRole, action)

        return item

    def _has_item_icon(self) -> bool:
        return any(not i.icon().isNull() for i in self._actions)

    def _create_item_icon(self, action: QAction) -> QIcon:
        # 如果前面的action中有icon了，那么即使这个action没有也要给一个透明的
        # 如果前面都没有icon，那就给个空的
        # 但感觉有一点不合理，万一第一个没有，第二个又有了，此时第一个已经没法修改了
        if self._has_item_icon():
            if action.icon().isNull():
                pixmap = QPixmap(self.view.iconSize())
                pixmap.fill(Qt.GlobalColor.transparent)
                icon = QIcon(pixmap)
            else:
                icon = action.icon()
        else:
            icon = QIcon()

        return icon

    def _adjust_item_text(self, item: QListWidgetItem, action: QAction) -> None:
        # TODO: leave sine space for shortcut key

        if not self._has_item_icon():
            item.setText(action.text())
            # width = 40 + self.view.fontMetrics().boundingRect(action.text()).width()
            width = 40 + self.view.fontMetrics().boundingRect(item.text()).width()
        else:
            item.setText(" " + action.text())
            width = 60 + self.view.fontMetrics().boundingRect(item.text()).width()

        item.setSizeHint(QSize(width, self._item_height))

    def exec(self, pos: QPoint, ani_type=MenuAnimationType.NONE) -> None:
        self.ani_manager = MenuAnimationManager.make(self, ani_type)
        self.ani_manager.exec(pos)

        self.show()

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        action: QAction = item.data(Qt.ItemDataRole.UserRole)

        self.view.clearSelection()
        self.close()

        action.trigger()


class MenuAnimationManager(QObject):
    managers = {}

    def __init__(self, menu: FMenu) -> None:
        super().__init__()

        self.menu = menu
        self.animation = QPropertyAnimation(menu, b"pos", menu)

        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.animation.valueChanged.connect(self.on_value_changed)
        self.animation.valueChanged.connect(self.update_menu_viewport)

    @classmethod
    def register(cls, name):
        def wrapper(manager):
            if name not in cls.managers:
                cls.managers[name] = manager

            return manager

        return wrapper

    @classmethod
    def make(cls, menu: FMenu, ani_type: MenuAnimationType):
        if ani_type not in cls.managers:
            raise ValueError(f"`{ani_type}` is not an invalid menu animation type.")

        return cls.managers[ani_type](menu)

    def exec(self, pos: QPoint):
        pass

    def _end_position(self, pos: QPoint):
        menu = self.menu
        rect = QApplication.screenAt(QCursor.pos()).availableGeometry()
        width, height = menu.width() + 5, menu.sizeHint().height()
        x = min(pos.x() - menu.layout().contentsMargins().left(), rect.right() - width)
        y = min(pos.y() - 4, rect.bottom() - height)
        return QPoint(x, y)

    def _menu_size(self):
        margins = self.menu.layout().contentsMargins()
        width = self.menu.view.width() + margins.left() + margins.right() + 120
        height = self.menu.view.height() + margins.top() + margins.bottom() + 20
        return width, height

    def on_value_changed(self):
        pass

    def update_menu_viewport(self) -> None:
        self.menu.view.viewport().update()
        self.menu.view.setAttribute(Qt.WidgetAttribute.WA_UnderMouse, True)
        event = QHoverEvent(QEvent.Type.HoverEnter, QPoint(), QPoint(1, 1))
        QApplication.sendEvent(self.menu.view, event)


@MenuAnimationManager.register(MenuAnimationType.NONE)
class MenuAnimationManagerNone(MenuAnimationManager):
    def exec(self, pos: QPoint):
        # self.menu.move(pos)
        self.menu.move(self._end_position(pos))


@MenuAnimationManager.register(MenuAnimationType.DROP_DOWN)
class MenuAnimationManagerDropDown(MenuAnimationManager):
    def exec(self, pos: QPoint):
        pos = self._end_position(pos)
        height = self.menu.height() + 5

        self.animation.setStartValue(pos - QPoint(0, height // 2))
        self.animation.setEndValue(pos)
        self.animation.start()

    def on_value_changed(self):
        width, height = self._menu_size()
        y = self.animation.endValue().y() - self.animation.currentValue().y()
        self.menu.setMask(QRegion(0, y, width, height))
