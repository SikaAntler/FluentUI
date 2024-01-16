from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from ..framesless import FramelessHelper
from ..utils import FluentStyleSheet


class FWidget(FramelessHelper, QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._set_window_flags(Qt.WindowType.Window)

        self.setContentsMargins(0, 32, 0, 0)  # 为TitleBar留空

        FluentStyleSheet.WINDOW.apply(self)
