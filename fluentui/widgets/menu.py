from enum import Enum

from PySide6.QtCore import (
    QEasingCurve,
    QModelIndex,
    QObject,
    QPersistentModelIndex,
    QPoint,
    QPropertyAnimation,
    QRectF,
    QSize,
    Qt,
)
from PySide6.QtGui import (
    QColor,
    QFontMetrics,
    QIcon,
    QKeySequence,
    QPainter,
    QPen,
    QPixmap,
    QRegion,
)
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QWidget,
)

from ..utils import FAction, FStyleSheet, get_screen_geometry, set_font


class MenuAnimationType(Enum):
    NONE = 0
    DROP_DOWN = 1
    PULL_UP = 2
    FADE_IN_DROP_DOWN = 3
    FADE_IN_DROP_UP = 4


class MenuItemDelegate(QStyledItemDelegate):
    @staticmethod
    def _is_seperator(index: QModelIndex | QPersistentModelIndex):
        return index.model().data(index, Qt.ItemDataRole.DecorationRole) == "seperator"

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        super().paint(painter, option, index)

        if not self._is_seperator(index):
            return

        painter.save()

        pen = QPen(QColor(0, 0, 0, 25), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        rect = option.rect
        painter.drawLine(0, rect.y() + 4, rect.width() + 12, rect.y() + 4)

        painter.restore()


class ShortcutMenuItemDelegate(MenuItemDelegate):
    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        super().paint(painter, option, index),

        if self._is_seperator(index):
            return

        action: FAction = index.data(Qt.ItemDataRole.UserRole)
        # if not isinstance(action, QAction) or action.shortcut().isEmpty():
        if action.shortcut().isEmpty():
            print("Action does not have shortcut")
            return

        painter.save()

        font = self.parent().font()
        painter.setFont(font)
        painter.setPen(QColor(0, 0, 0, 153))

        fm = QFontMetrics(font)
        shortcut = action.shortcut().toString(QKeySequence.SequenceFormat.NativeText)

        sw = fm.boundingRect(shortcut).width() + 1  # +1是为了修正字被遮住了一点儿
        painter.translate(option.rect.width() - sw - 20, 0)

        rect = QRectF(0, option.rect.y(), sw, option.rect.height())
        painter.drawText(
            rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, shortcut
        )

        painter.restore()


class MenuActionListWidget(QListWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)

        self.setViewportMargins(0, 6, 0, 6)
        self.setIconSize(QSize(16, 16))
        self.setTextElideMode(Qt.TextElideMode.ElideNone)  # 否则会有...出现
        self.setDragEnabled(False)
        self.setMouseTracking(True)

        # 否则会出现滚动条，但即使设置Off依然可以滚动
        # self.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setEnabled(False)
        self.horizontalScrollBar().setEnabled(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setItemDelegate(ShortcutMenuItemDelegate(self))

        FStyleSheet.MENU.apply(self)
        set_font(self, font_size=10)

    def addItem(self, item: QListWidgetItem) -> None:
        super().addItem(item)
        self.adjustSize()

    def insertItem(self, row: int, item: QListWidgetItem) -> None:
        super().insertItem(row, item)
        self.adjustSize()

    def takeItem(self, row: int) -> QListWidgetItem:
        item = super().takeItem(row)
        self.adjustSize()

        return item

    def adjustSize(self) -> None:
        size = QSize(1, 1)
        for i in range(self.count()):
            s = self.item(i).sizeHint()
            size.setWidth(max(size.width(), s.width(), 1))
            size.setHeight(max(size.height() + s.height(), 1))

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
        # 背景透明, 即使margins设置全0，因为圆角的缘故也会有背景色
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.hlyt = QHBoxLayout(self)
        self.hlyt.setContentsMargins(12, 8, 12, 20)

        self.view = MenuActionListWidget(self)
        self.hlyt.addWidget(self.view, 1, Qt.AlignmentFlag.AlignCenter)

        self.shadow_effect = QGraphicsDropShadowEffect(self.view)
        self.shadow_effect.setBlurRadius(30)
        self.shadow_effect.setOffset(0, 8)
        self.shadow_effect.setColor(QColor(0, 0, 0, 30))
        self.view.setGraphicsEffect(self.shadow_effect)

        self._actions = []  # type: list[FAction]

        self._item_height = 28

        self.view.itemClicked.connect(self._on_item_clicked)

        self.ani_manager = None

        # TODO: 增加SubMenu功能，需要写的比较多

        # TODO: 原代码对于是否要加icon的逻辑有问题，比如第一个没加，第二个相加怎么办

        # TODO: 增加菜单的弹出动画

        # TODO: 对面对于view、viewport和margins的概念比较迷糊，比如在代码中有如下情况，
        #  self.view.viewportMargins()=(0, 6, 0, 6) 这是初始化时设置的
        #  self.view.contentsMargins()=(1, 1, 1, 1) 这个又影响什么就不清楚了

    def addAction(self, action: FAction) -> None:
        item = self._create_action_item(action)
        self.view.addItem(item)
        self.adjustSize()

    def addActions(self, actions: list[FAction]) -> None:
        for action in actions:
            self.addAction(action)

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

    def exec(self, pos: QPoint, ani_type=MenuAnimationType.NONE) -> None:
        self.ani_manager = MenuAnimationManager.make(self, ani_type)
        self.ani_manager.exec(pos)

        self.show()

    def _create_action_item(self, action: FAction) -> QListWidgetItem:
        self._actions.append(action)

        icon = self._create_item_icon(action)
        item = QListWidgetItem(icon, action.text())

        self._adjust_item_text(item, action)

        item.setData(Qt.ItemDataRole.UserRole, action)

        return item

    def _has_item_icon(self) -> bool:
        return any(a.icon() is not None for a in self._actions)

    def _create_item_icon(self, action: FAction) -> QIcon:
        # 如果前面的action中有icon了，那么即使这个action没有也要给一个透明的
        # 如果前面都没有icon，那就给个空的
        # 但感觉有一点不合理，万一第一个没有，第二个又有了，此时第一个已经没法修改了
        if self._has_item_icon():
            if action.icon() is None:
                pixmap = QPixmap(self.view.iconSize())
                pixmap.fill(Qt.GlobalColor.transparent)
                icon = QIcon(pixmap)
            else:
                icon = action.icon().icon()
        else:
            icon = QIcon()

        return icon

    def _longest_shortcut_width(self) -> int:
        longest_width = 0
        for action in self._actions:
            shortcut = action.shortcut().toString(
                QKeySequence.SequenceFormat.NativeText
            )
            width = self.view.fontMetrics().boundingRect(shortcut).width()
            longest_width = max(longest_width, width)

        return longest_width

    def _adjust_item_text(self, item: QListWidgetItem, action: FAction) -> int:
        # TODO: leave sine space for shortcut key

        sw = self._longest_shortcut_width()
        sw = sw + 22 if sw != 0 else 0

        text = action.text()
        fm = self.view.fontMetrics()
        if not self._has_item_icon():
            item.setText(text)
            width = 40 + fm.boundingRect(text).width() + sw
        else:
            item.setText(" " + text)
            space = 4 - fm.boundingRect(" ").width()
            width = 60 + fm.boundingRect(text).width() + sw + space

        item.setSizeHint(QSize(width, self._item_height))

        return width

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        action: FAction = item.data(Qt.ItemDataRole.UserRole)
        if action not in self._actions or not action.isEnabled():
            return

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
        self.animation.valueChanged.connect(self._on_value_changed)
        self.animation.valueChanged.connect(self._update_menu_viewport)

    @classmethod
    def register(cls, name):
        def wrapper(manager):
            if name not in cls.managers:
                cls.managers[name] = manager

            return manager

        return wrapper

    @classmethod
    def make(cls, menu: FMenu, ani_type: MenuAnimationType) -> "MenuAnimationManager":
        if ani_type not in cls.managers:
            raise ValueError(f"`{ani_type}` is an invalid menu animation type")

        return cls.managers[ani_type](menu)

    def exec(self, pos: QPoint) -> None:
        raise NotImplementedError

    def _end_position(self, pos: QPoint) -> QPoint:
        menu = self.menu
        geometry = get_screen_geometry()
        w, h = menu.width() + 5, menu.sizeHint().height()
        x = min(pos.x() - menu.layout().contentsMargins().left(), geometry.right() - w)
        y = min(pos.y() - 4, geometry.bottom() - h + 10)

        return QPoint(x, y)

    def _menu_size(self) -> tuple[int, int]:
        margins = self.menu.layout().contentsMargins()
        w = self.menu.view.width() + margins.left() + margins.right() + 120
        h = self.menu.view.height() + margins.top() + margins.bottom() + 20

        return w, h

    def _on_value_changed(self) -> None:
        raise NotImplementedError

    def _update_menu_viewport(self) -> None:
        self.menu.view.viewport().update()
        self.menu.view.setAttribute(Qt.WidgetAttribute.WA_UnderMouse, True)
        # event = QHoverEvent(QEvent.Type.HoverEnter, QPoint(), QPoint(1, 1))
        # QApplication.sendEvent(self.menu.view, event)


@MenuAnimationManager.register(MenuAnimationType.NONE)
class MenuAnimationNone(MenuAnimationManager):
    def exec(self, pos: QPoint) -> None:
        self.menu.move(self._end_position(pos))


@MenuAnimationManager.register(MenuAnimationType.DROP_DOWN)
class MenuAnimationDropDown(MenuAnimationManager):
    def exec(self, pos: QPoint) -> None:
        pos = self._end_position(pos)
        height = self.menu.height() + 5

        self.animation.setStartValue(pos - QPoint(0, height // 2))
        self.animation.setEndValue(pos)
        self.animation.start()

    def _on_value_changed(self) -> None:
        width, height = self._menu_size()
        y = self.animation.endValue().y() - self.animation.currentValue().y()
        self.menu.setMask(QRegion(0, y, width, height))
