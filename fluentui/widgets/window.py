from ..framesless import FramelessMainWindow
from ..utils import FStyleSheet


class FMainWindow(FramelessMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        FStyleSheet.WINDOW.apply(self)
