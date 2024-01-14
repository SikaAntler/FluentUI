from PySide6.QtCore import Qt
from PySide6.QtWidgets import QRadioButton

from ..utils import FluentStyleSheet, set_font


class FRadioButton(QRadioButton):
    def __init__(self, text: str, parent=None):
        super().__init__(text=text, parent=parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        FluentStyleSheet.RADIO_BUTTON.apply(self)

        set_font(self, font_size=12)
