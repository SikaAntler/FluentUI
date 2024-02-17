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


class FStyleSheet(StyleSheet, Enum):
    BUTTON = "button"
    DIALOG = "dialog"
    LINE_EDIT = "line_edit"
    GROUP_BOX = "group_box"
    LIST_VIEW = "list_view"
    MENU = "menu"
    NAVIGATION = "navigation"
    RADIO_BUTTON = "radio_button"
    SETTING_CARD = "setting_card"
    TOOL_TIP = "tool_tip"
    WINDOW = "window"

    def path(self) -> str:
        return f":/fluentui/qss/{self.value}.qss"
