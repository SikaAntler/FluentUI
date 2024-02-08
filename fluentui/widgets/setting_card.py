from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, QIcon, QPainter, QPaintEvent, Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ..utils import FStyleSheet, Icon, draw_icon, set_font
from .button import FPushButton
from .slider import FSlider
from .switch_button import FSwitchButton, IndicatorPosition


class SettingIcon(QWidget):
    def __init__(self, icon: QIcon | Icon, parent=None) -> None:
        super().__init__(parent=parent)

        self._icon = icon

    def icon(self) -> QIcon | Icon:
        return self._icon

    def setIcon(self, icon: QIcon | Icon) -> None:
        self._icon = icon
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        if not self.isEnabled():
            painter.setOpacity(0.36)

        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )
        draw_icon(self._icon, painter, self.rect())


class SettingCard(QWidget):
    def __init__(
        self, icon: QIcon | Icon, title: str = "", content: str = "", parent=None
    ):
        super().__init__(parent=parent)

        self.setFixedHeight(70 if content != "" else 50)

        self.hlyt = QHBoxLayout(self)
        self.hlyt.setContentsMargins(16, 0, 0, 0)
        self.hlyt.setSpacing(0)
        self.hlyt.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.vlyt = QVBoxLayout(self)
        self.vlyt.setContentsMargins(0, 0, 0, 0)
        self.vlyt.setSpacing(0)
        self.vlyt.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.lbl_icon = SettingIcon(icon, self)
        self.lbl_icon.setFixedSize(20, 20)
        self.hlyt.addWidget(self.lbl_icon, 0, Qt.AlignmentFlag.AlignLeft)
        self.hlyt.addSpacing(16)

        self.hlyt.addLayout(self.vlyt)

        self.lbl_title = QLabel(title, self)
        self.lbl_title.setObjectName("lbl_title")
        set_font(self.lbl_title, font_size=11)
        self.vlyt.addWidget(self.lbl_title, 0, Qt.AlignmentFlag.AlignLeft)

        self.lbl_content = QLabel(content, self)
        self.lbl_content.setObjectName("lbl_content")
        set_font(self.lbl_content, font_size=9)
        self.vlyt.addWidget(self.lbl_content, 0, Qt.AlignmentFlag.AlignLeft)
        if content == "":
            self.lbl_content.hide()

        self.hlyt.addSpacing(16)
        self.hlyt.addStretch(1)

        FStyleSheet.SETTING_CARD.apply(self)

    def title(self) -> str:
        return self.lbl_title.text()

    def setTitle(self, title: str) -> None:
        self.lbl_title.setText(title)

    def content(self) -> str:
        return self.lbl_content.text()

    def setContent(self, content: str) -> None:
        self.lbl_content.setText(content)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(255, 255, 255, 170))
        painter.setPen(QColor(0, 0, 0, 19))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class PushSettingCard(SettingCard):
    clicked = Signal()

    def __init__(
        self,
        text: str,
        icon: QIcon | Icon,
        title: str = "",
        content: str = "",
        parent=None,
    ) -> None:
        super().__init__(icon=icon, title=title, content=content, parent=parent)

        self.btn = FPushButton(text, self)
        set_font(self.btn, font_size=10)
        self.hlyt.addWidget(self.btn, 0, Qt.AlignmentFlag.AlignRight)
        self.hlyt.addSpacing(16)
        self.btn.clicked.connect(self.clicked)


class SwitchSettingCard(SettingCard):
    checkedChanged = Signal()

    def __init__(
        self,
        position: IndicatorPosition,
        icon: QIcon | Icon,
        title: str = "",
        content: str = "",
        parent=None,
    ) -> None:
        super().__init__(icon=icon, title=title, content=content, parent=parent)

        self.switch_button = FSwitchButton(position, self)
        self.hlyt.addWidget(self.switch_button, 0, Qt.AlignmentFlag.AlignRight)
        self.hlyt.addSpacing(16)

        self.switch_button.checkedChanged.connect(self.checkedChanged)

    def isChecked(self) -> bool:
        return self.switch_button.isChecked()

    def setChecked(self, isChecked) -> None:
        self.switch_button.setChecked(isChecked)


class SliderSettingCard(SettingCard):
    valueChanged = Signal(int)

    def __init__(
        self,
        icon: QIcon | Icon,
        title: str = "",
        content: str = "",
        parent=None,
    ) -> None:
        super().__init__(icon=icon, title=title, content=content, parent=parent)

        self.lbl_value = QLabel(self)
        self.hlyt.addWidget(self.lbl_value, 0, Qt.AlignmentFlag.AlignRight)
        self.hlyt.addSpacing(6)

        self.slider = FSlider(Qt.Orientation.Horizontal, self)
        self.hlyt.addWidget(self.slider, 0, Qt.AlignmentFlag.AlignRight)
        self.hlyt.addSpacing(16)

        self.slider.valueChanged.connect(self._on_slider_valueChanged)

    def value(self) -> int:
        return self.slider.value()

    def setValue(self, value: int) -> None:
        self.lbl_value.setNum(value)
        self.lbl_value.adjustSize()
        self.slider.setValue(value)

    def _on_slider_valueChanged(self, value: int) -> None:
        self.setValue(value)
        self.valueChanged.emit(value)


class SettingCardGroup(QWidget):
    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent=parent)

        self.vlyt = QVBoxLayout(self)
        self.vlyt.setContentsMargins(0, 0, 0, 0)
        self.vlyt.setSpacing(0)
        self.vlyt.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.lbl_title = QLabel(title, self)
        set_font(self.lbl_title, font_size=16)
        self.vlyt.addWidget(self.lbl_title, Qt.AlignmentFlag.AlignLeft)
        self.vlyt.addSpacing(12)

        FStyleSheet.SETTING_CARD.apply(self)

    def addSettingCard(self, card: SettingCard) -> None:
        card.setParent(self)
        self.vlyt.addWidget(card)
