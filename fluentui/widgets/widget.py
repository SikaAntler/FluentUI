from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from ..framesless import FramelessHelper


class FWidget(FramelessHelper, QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._set_window_flags(Qt.WindowType.Window)
