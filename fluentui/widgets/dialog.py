from ..framesless import FramelessDialog
from ..utils import FluentStyleSheet


class FDialog(FramelessDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        # self._set_window_flags(Qt.WindowType.Dialog)

        self.setContentsMargins(0, 32, 0, 0)

        FluentStyleSheet.WINDOW.apply(self)
