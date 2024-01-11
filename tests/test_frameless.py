from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QWidget

from fluentui.framesless import FramelessHelper


class FramelessDialog(FramelessHelper, QDialog):
    def __init__(self):
        super().__init__()

        self._set_window_flags(Qt.WindowType.Dialog)

        self.setWindowTitle("FramelessDialog")
        self.resize(400, 300)


class FramelessWindow(FramelessHelper, QMainWindow):
    def __init__(self):
        super().__init__()

        self._set_window_flags(Qt.WindowType.Window)

        self.setMenuWidget(self.title_bar)

        self.setWindowTitle("FramelessWindow")
        self.resize(1187, 667)


class FramelessWidget(FramelessHelper, QWidget):
    def __init__(self):
        super().__init__()

        self._set_window_flags(Qt.WindowType.Window)

        self.setWindowTitle("FramelessWidget")
        self.resize(960, 540)


if __name__ == "__main__":
    app = QApplication()
    dialog = FramelessDialog()
    window = FramelessWindow()
    widget = FramelessWidget()
    dialog.show()
    window.show()
    widget.show()
    app.exec()
