from enum import Enum

from PySide6.QtCore import QFile
from PySide6.QtWidgets import QWidget


class StyleSheet:
    def apply(self, widget: QWidget) -> None:
        style_sheet = self.read_qss()
        widget.setStyleSheet(style_sheet)

    def path(self) -> str:
        raise NotImplementedError

    def read_qss(self) -> str:
        file = QFile(self.path())
        file.open(QFile.ReadOnly)
        qss = str(file.readAll(), encoding="utf-8")
        file.close()
        return qss


class FluentStyleSheet(StyleSheet, Enum):
    BUTTON = "button"
    GROUP_BOX = "group_box"
    LIST_WIDGET = "list_widget"
    MENU = "menu"
    RADIO_BUTTON = "radio_button"
    WINDOW = "window"

    def path(self) -> str:
        return f":/fluentui/qss/{self.value}.qss"
