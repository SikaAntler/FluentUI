from ..framesless import FramelessWidget
from ..utils import FStyleSheet


class FWidget(FramelessWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        # self._set_window_flags(Qt.WindowType.Window)

        self.setContentsMargins(0, 32, 0, 0)  # 为TitleBar留空

        FStyleSheet.WINDOW.apply(self)
