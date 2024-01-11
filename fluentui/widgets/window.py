from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from ..framesless import FramelessHelper


class FMainWindow(FramelessHelper, QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self._set_window_flags(Qt.WindowType.Window)

        self.setMenuWidget(self.title_bar)
