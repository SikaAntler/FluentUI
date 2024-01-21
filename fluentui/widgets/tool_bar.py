from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget

from ..utils import FAction, draw_icon, set_font
from .button import ToolButton


class FToolButton(ToolButton):
    def __init__(self, action: FAction, parent=None) -> None:
        super().__init__(icon=action.icon(), text=action.text(), parent=parent)

        self._action = action
        self._on_action_changed()
        action.changed.connect(self._on_action_changed)
        # 点击此button时同时改变action状态
        self.clicked.connect(action.toggle)
        self._is_tight = False

    def action(self) -> FAction:
        return self._action

    def setTight(self, is_tight: bool) -> None:
        self._is_tight = is_tight
        self.update()

    def isTight(self) -> bool:
        return self._is_tight

    def sizeHint(self) -> QSize:
        if self._is_icon_only():
            return QSize(36, 24) if self._is_tight else QSize(48, 34)

        # get the width of text
        tw = self.fontMetrics().boundingRect(self._text).width()

        style = self.toolButtonStyle()
        if style == Qt.ToolButtonStyle.ToolButtonTextOnly:
            return QSize(tw + 32, 34)
        elif style == Qt.ToolButtonStyle.ToolButtonTextBesideIcon:
            return QSize(tw + 47, 34)
        elif style == Qt.ToolButtonStyle.ToolButtonTextUnderIcon:
            return QSize(tw + 32, 50)

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制QSS样式，且因QSS绘制的是背景色，所以需放在开头
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.TextAntialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
        )

        if self.isChecked():
            painter.setPen(QColor("white"))
            state = QIcon.State.On
        else:
            painter.setPen(QColor("black"))
            state = QIcon.State.Off

        if not self.isEnabled():
            # painter.setOpacity(0.43)
            painter.setOpacity(0.9)  # 原代码一顿super调用结果似乎就是这个
        elif self._is_pressed:
            painter.setOpacity(0.63)

        style = self.toolButtonStyle()
        iw, ih = self.iconSize().toTuple()

        if self._is_icon_only():
            x = (self.width() - iw) // 2
            y = (self.height() - ih) // 2
            draw_icon(self._icon, painter, QRect(x, y, iw, ih), state)
        elif style == Qt.ToolButtonStyle.ToolButtonTextOnly:
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self._text)
        elif style == Qt.ToolButtonStyle.ToolButtonTextBesideIcon:
            y = (self.height() - ih) // 2
            draw_icon(self._icon, painter, QRect(11, y, iw, ih), state)
            painter.drawText(
                QRect(26, 0, self.width() - 26, self.height()),
                Qt.AlignmentFlag.AlignCenter,
                self._text,
            )
        elif style == Qt.ToolButtonStyle.ToolButtonTextUnderIcon:
            x = (self.width() - iw) // 2
            # super()._draw_icon(painter, QRect(x, 9, iw, ih))
            draw_icon(self._icon, painter, QRect(x, 9, iw, ih))
            painter.drawText(
                QRect(0, ih + 13, self.width(), self.height() - ih - 13),
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop,
                self._text,
            )

    def _is_icon_only(self) -> bool:
        return self.toolButtonStyle() in [
            Qt.ToolButtonStyle.ToolButtonIconOnly,
            Qt.ToolButtonStyle.ToolButtonFollowStyle,
        ]

    def _on_action_changed(self) -> None:
        self.setIcon(self._action.icon())
        self.setText(self._action.text())
        self.setToolTip(self._action.toolTip())

        self.setCheckable(self._action.isCheckable())
        self.setChecked(self._action.isChecked())
        self.setEnabled(self._action.isEnabled())


class FToolSeparator(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setFixedSize(9, 34)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0, 15))
        painter.drawLine(5, 2, 5, self.height() - 2)


class FToolBar(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self._widgets = []  # type: list[QWidget]

        self._tool_button_style = Qt.ToolButtonStyle.ToolButtonIconOnly
        self._is_button_tight = False
        self._icon_size = QSize(24, 24)  # 原代码是16，但svg图片不同，这里用16显得有些小
        self._font_size = 10
        self._spacing = 4

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def addAction(self, action: FAction) -> None:
        super().addAction(action)

        button = self._create_button(action)
        button.setToolTip(action.toolTip())
        self._insert_widget_to_layout(len(self._widgets), button)

    def addSeparator(self) -> None:
        separator = FToolSeparator()
        self._insert_widget_to_layout(len(self._widgets), separator)

    def _create_button(self, action: FAction) -> FToolButton:
        button = FToolButton(action)
        button.setToolButtonStyle(self._tool_button_style)
        button.setTight(self._is_button_tight)
        button.setIconSize(self._icon_size)
        set_font(button, font_size=self._font_size)

        return button

    def _insert_widget_to_layout(self, index: int, widget: QWidget) -> None:
        widget.setParent(self)
        widget.show()

        self._widgets.insert(index, widget)
        self.setFixedHeight(max(w.height() for w in self._widgets))
        self.updateGeometry()

    def buttons(self) -> list[FToolButton]:
        return [btn for btn in self._widgets if isinstance(btn, FToolButton)]

    def setToolButtonStyle(self, style: Qt.ToolButtonStyle) -> None:
        if style == self._tool_button_style:
            return

        self._tool_button_style = style
        for btn in self.buttons():
            btn.setToolButtonStyle(style)

    def _visible_widgets(self) -> list[QWidget]:
        return self._widgets

    def updateGeometry(self) -> None:
        x = self.contentsMargins().left()
        h = self.height()

        widgets = self._visible_widgets()
        for widget in widgets:
            widget.move(x, (h - widget.height()) // 2)
            x += widget.width() + self._spacing
