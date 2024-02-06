from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPlainTextEdit,
)

from fluentui.widgets import FScrollBar
from fluentui.utils import set_font


class PlainTextEdit(QPlainTextEdit):
    def __init__(self, orientation: Qt.Orientation, parent=None) -> None:
        super().__init__(parent=parent)

        self.scroll_bar = FScrollBar(orientation, self)
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

        self.text_edit_v = PlainTextEdit(Qt.Orientation.Vertical, self)
        self.text_edit_v.setPlainText(
            "q\nw\ne\nr\nt\ny\nu\ni\no\np\na\ns\nd\nf\ng\nh\nj\nk\nl\n"
        )
        self.vlyt.addWidget(self.text_edit_v)

        self.text_edit_h = PlainTextEdit(Qt.Orientation.Horizontal, self)
        self.text_edit_h.setPlainText(f"{'qwertyuiopasdfghjkl'*10}")
        self.vlyt.addWidget(self.text_edit_h)


if __name__ == "__main__":
    app = QApplication()
    scroll_bar = TestScrollBar()
    scroll_bar.show()
    app.exec()
