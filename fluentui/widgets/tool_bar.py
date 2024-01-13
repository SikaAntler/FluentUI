from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QAction, QColor, QPainter, QPaintEvent, QMouseEvent
from PySide6.QtWidgets import QFrame, QWidget

from ..utils import set_font
from .button import ToolButton


class FToolButton(ToolButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        self._action = None
        self._is_pressed = False
        self._is_tight = False

    def isTight(self) -> bool:
        return self._is_tight

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = False
        super().mouseReleaseEvent(event)

    def setAction(self, action: QAction) -> None:
        self._action = action
        self.clicked.connect(action.trigger)
        action.changed.connect(self._on_action_changed)
        action.toggled.connect(self._on_action_toggled)

    def setTight(self, is_tight: bool) -> None:
        self._is_tight = is_tight
        self.update()

    def _on_action_changed(self) -> None:
        self.setIcon(self._action.icon())
        self.setText(self._action.text())
        self.setToolTip(self._action.toolTip())

    def _on_action_toggled(self, is_checked: bool) -> None:
        self.setChecked(True)
        self.setChecked(is_checked)

    def _is_icon_only(self) -> bool:
        return self.toolButtonStyle() in [
            Qt.ToolButtonStyle.ToolButtonIconOnly,
            Qt.ToolButtonStyle.ToolButtonFollowStyle,
        ]

    def sizeHint(self) -> QSize:
        style = self.toolButtonStyle()

        # get the width of text
        tw = self.fontMetrics().boundingRect(self.text()).width()

        if self._is_icon_only():
            return QSize(36, 34) if self._is_tight else QSize(48, 34)
        elif style == Qt.ToolButtonStyle.ToolButtonTextBesideIcon:
            return QSize(tw + 47, 34)
        elif style == Qt.ToolButtonStyle.ToolButtonTextOnly:
            return QSize(tw + 32, 34)
        else:  # ToolButtonTextUnderIcon
            return QSize(tw + 32, 50)

    def paintEvent(self, arg__1: QPaintEvent) -> None:
        super().paintEvent(arg__1)

        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.TextAntialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
        )

        if not self.isEnabled():
            painter.setOpacity(0.43)
        elif self._is_pressed:
            painter.setOpacity(0.63)

        style = self.toolButtonStyle()
        iw, ih = self.iconSize().width(), self.iconSize().height()

        if self._is_icon_only():
            x = (self.width() - iw) // 2
            y = (self.height() - ih) // 2
            self._icon.paint(
                painter,
                QRect(x, y, iw, ih),
                Qt.AlignmentFlag.AlignCenter,
            )
        elif style == Qt.ToolButtonStyle.ToolButtonTextOnly:
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        elif style == Qt.ToolButtonStyle.ToolButtonTextBesideIcon:
            pass
        elif style == Qt.ToolButtonStyle.ToolButtonTextUnderIcon:
            pass


class FToolSeparator(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setFixedSize(9, 34)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0, 15))
        painter.drawLine(5, 2, 5, self.height() - 2)


class FToolBar(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self._widgets = []  # type: list[QWidget]

        self._tool_button_style = Qt.ToolButtonStyle.ToolButtonIconOnly
        self._is_button_tight = False
        self._icon_size = QSize(24, 24)  # 原代码是16，但svg图片不同，这里用16显得有些小
        self._spacing = 4

        # set_font(self, font_size=12)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def addAction(self, action: QAction) -> None:
        super().addAction(action)

        button = self._create_button(action)
        button.setToolTip(action.toolTip())
        self._insert_widget_to_layout(len(self._widgets), button)

    def addSeparator(self) -> None:
        separator = FToolSeparator()
        self._insert_widget_to_layout(len(self._widgets), separator)

    def _create_button(self, action: QAction) -> FToolButton:
        button = FToolButton()
        button.setIcon(action.icon())
        button.setText(action.text())
        button.setAction(action)
        button.setToolButtonStyle(self._tool_button_style)
        button.setTight(self._is_button_tight)
        button.setIconSize(self._icon_size)
        button.setFont(self.font())

        return button

    def _insert_widget_to_layout(self, index: int, widget: QWidget) -> None:
        widget.setParent(self)
        widget.show()

        self._widgets.insert(index, widget)
        self.setFixedHeight(max(w.height() for w in self._widgets))
        self.updateGeometry()

    def command_buttons(self) -> list[FToolButton]:
        return [btn for btn in self._widgets if isinstance(btn, FToolButton)]

    def set_tool_button_style(self, style: Qt.ToolButtonStyle) -> None:
        if style == self._tool_button_style:
            return

        self._tool_button_style = style
        for btn in self.command_buttons():
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
            # widget.show()
