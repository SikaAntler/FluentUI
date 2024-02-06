from string import ascii_uppercase

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from fluentui.utils import set_font
from fluentui.widgets import FScrollBar, FSmoothScrollBar


class PlainTextEdit(QPlainTextEdit):
    def __init__(self, smooth: bool, parent=None) -> None:
        super().__init__(parent=parent)

        if smooth:
            self.scroll_bar_v = FSmoothScrollBar(Qt.Orientation.Vertical, self)
            self.scroll_bar_h = FSmoothScrollBar(Qt.Orientation.Horizontal, self)
        else:
            self.scroll_bar_v = FScrollBar(Qt.Orientation.Vertical, self)
            self.scroll_bar_h = FScrollBar(Qt.Orientation.Horizontal, self)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        set_font(self)


class TestScrollBar(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Test Scroll Bar")
        self.resize(400, 300)

        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)
        self.vlyt = QVBoxLayout(self.widget_central)

        test_text = [ascii_uppercase * 3]
        for i in range(1, 10):
            text = ascii_uppercase[26 - i : 26] + ascii_uppercase[: 26 - i]
            test_text.append(text * 3)
        test_text = "\n".join(test_text)

        self.text_edit = PlainTextEdit(False, self)
        self.text_edit.setPlainText(test_text)
        self.vlyt.addWidget(self.text_edit)

        self.smooth_text_edit = PlainTextEdit(True, self)
        self.smooth_text_edit.setPlainText(test_text)
        self.vlyt.addWidget(self.smooth_text_edit)


if __name__ == "__main__":
    app = QApplication()
    scroll_bar = TestScrollBar()
    scroll_bar.show()
    app.exec()
