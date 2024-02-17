from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ..framesless import FramelessDialog
from ..utils import FIcon, FStyleSheet, Icon, draw_icon, set_font
from ..widgets import FPushButton, PrimaryPushButton


class FDialog(FramelessDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setContentsMargins(0, 32, 0, 0)

        # FStyleSheet.WINDOW.apply(self)


class MessageIcon(QWidget):
    def __init__(self, icon: Icon, parent=None, fill: str = None) -> None:
        super().__init__(parent=parent)

        self._icon = icon
        self._fill = fill

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )
        draw_icon(self._icon, painter, self.rect(), fill=self._fill)


class FMessageBox(FramelessDialog):
    def __init__(
        self,
        icon: Icon,
        title: str,
        text: str,
        parent=None,
        fill: str = None,
        auto_exec: bool = False,
    ) -> None:
        super().__init__(parent=parent)

        # 与Qt自带的QMessage不同的是：
        # 1. 没有TitleBar，因此也就没有WindowIcon和WindowTitle了
        # 2. title放到下面显示，和text呈上下分布
        # 3. 无法自定义按钮

        self.title_bar.hide()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._hlyt = QHBoxLayout(self)
        self._hlyt.setContentsMargins(12, 10, 12, 20)
        self._hlyt.setSpacing(0)

        self.widget = QWidget(self)
        self.widget.setObjectName("widget")
        self._hlyt.addWidget(self.widget)

        self._set_shadow_effect()

        self.vlyt = QVBoxLayout(self.widget)
        self.vlyt.setContentsMargins(1, 1, 1, 1)
        self.vlyt.setSpacing(0)

        self.widget_contents = QWidget(self)
        self.glyt_content = QGridLayout(self.widget_contents)
        self.lbl_icon = MessageIcon(icon, self, fill)
        self.lbl_title = QLabel(title, self)
        self.lbl_text = QLabel(text, self)
        self._init_content()

        self.widget_buttons = QWidget(self)
        self.hlyt_buttons = QHBoxLayout(self.widget_buttons)
        self.btn_accept = PrimaryPushButton("确认", self)
        self.btn_reject = FPushButton("取消", self)
        self._init_buttons()

        self.btn_accept.clicked.connect(self.accept)
        self.btn_reject.clicked.connect(self.reject)

        FStyleSheet.DIALOG.apply(self)

        if auto_exec:
            self.exec()

        # TODO: 系统音效和闪烁效果

    def _set_shadow_effect(self) -> None:
        shadow_effect = QGraphicsDropShadowEffect(self.widget)
        shadow_effect.setBlurRadius(60)
        shadow_effect.setOffset(0, 10)
        shadow_effect.setColor(QColor(0, 0, 0, 50))
        self.widget.setGraphicsEffect(None)
        self.widget.setGraphicsEffect(shadow_effect)

    def _init_content(self) -> None:
        self.widget_contents.setObjectName("widget_contents")
        self.vlyt.addWidget(self.widget_contents, 1)

        self.glyt_content.setContentsMargins(12, 12, 12, 12)
        self.glyt_content.setSpacing(12)

        self.lbl_icon.setFixedSize(48, 48)
        self.glyt_content.addWidget(
            self.lbl_icon, 0, 0, 2, 1, Qt.AlignmentFlag.AlignCenter
        )

        set_font(self.lbl_title, font_size=18)
        self.glyt_content.addWidget(self.lbl_title, 0, 1, Qt.AlignmentFlag.AlignCenter)

        set_font(self.lbl_text)
        self.glyt_content.addWidget(self.lbl_text, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.glyt_content.setRowStretch(0, 1)
        self.glyt_content.setRowStretch(1, 0)
        self.glyt_content.setColumnStretch(0, 0)
        self.glyt_content.setColumnStretch(1, 1)

    def _init_buttons(self) -> None:
        self.widget_buttons.setObjectName("widget_buttons")
        self.vlyt.addWidget(self.widget_buttons, 0)

        self.hlyt_buttons.setContentsMargins(12, 12, 12, 12)
        self.hlyt_buttons.setSpacing(12)

        self.hlyt_buttons.addWidget(self.btn_accept)
        self.hlyt_buttons.addWidget(self.btn_reject)

    @classmethod
    def question(cls, parent, title: str, text: str) -> "FMessageBox":
        return cls(FIcon.QUESTION_CIRCLE, title, text, parent, "#30a75b", True)

    @classmethod
    def information(cls, parent, title: str, text: str) -> "FMessageBox":
        return cls(FIcon.INFO, title, text, parent, "#0b7ad4", True)

    @classmethod
    def warning(cls, parent, title: str, text: str) -> "FMessageBox":
        return cls(FIcon.WARNING, title, text, parent, "#f78a4c", True)

    @classmethod
    def critical(cls, parent, title: str, text: str) -> "FMessageBox":
        return cls(FIcon.ERROR_CIRCLE, title, text, parent, "#f14d85", True)
