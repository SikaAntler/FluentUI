from ..framesless import FramelessMainWindow
from ..utils import FluentStyleSheet


class FMainWindow(FramelessMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        FluentStyleSheet.WINDOW.apply(self)
