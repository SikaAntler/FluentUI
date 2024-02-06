from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from fluentui.widgets import FLineEdit, FPlainTextEdit, FPushButton


class TestFLineEdit(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Test FLineEdit")
        self.resize(300, 200)

        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)
        self.hlyt = QHBoxLayout(self.widget_central)

        self.line_edit = FLineEdit(self)
        self.line_edit.setPlaceholderText("请输入标签")
        self.hlyt.addWidget(self.line_edit, 1)

        self.btn_search = FPushButton(text="搜索")
        self.hlyt.addWidget(self.btn_search, 0)


class TestFPlainTextEdit(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Test FPlainTextEdit")
        self.resize(400, 400)

        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)
        self.vlyt = QVBoxLayout(self.widget_central)

        self.text_edit = FPlainTextEdit(self)
        self.text_edit.setReadOnly(False)
        self.vlyt.addWidget(self.text_edit, 1)

        self.btn_edit = FPushButton(text="编辑", parent=self)
        self.vlyt.addWidget(self.btn_edit, 0)


if __name__ == "__main__":
    app = QApplication()
    line_edit = TestFLineEdit()
    line_edit.show()
    text_edit = TestFPlainTextEdit()
    text_edit.show()
    app.exec()
