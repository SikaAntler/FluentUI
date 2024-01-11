from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog

from ..framesless import FramelessHelper


class FDialog(FramelessHelper, QDialog):
    def __init__(self) -> None:
        super().__init__()

        self._set_window_flags(Qt.WindowType.Dialog)
