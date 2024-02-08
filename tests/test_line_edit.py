from string import ascii_uppercase

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QGridLayout,
    QWidget,
)

from fluentui.widgets import FLineEdit, FPlainTextEdit, FPushButton


class TestEdit(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Test Edit")
        self.resize(400, 300)

        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)
        self.glyt = QGridLayout(self.widget_central)

        self.line_edit = FLineEdit(self)
        self.line_edit.setPlaceholderText("请输入标签")
        self.glyt.addWidget(self.line_edit, 0, 0, 1, 1)

        self.btn_search = FPushButton("搜索", self)
        self.glyt.addWidget(self.btn_search, 0, 1, 1, 1)

        test_text = [ascii_uppercase * 3]
        for i in range(1, 26):
            text = ascii_uppercase[26 - i : 26] + ascii_uppercase[: 26 - i]
            test_text.append(text * 3)
        test_text = "\n".join(test_text)

        self.text_edit = FPlainTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(FPlainTextEdit.LineWrapMode.NoWrap)
        self.text_edit.setPlainText(test_text)
        self.glyt.addWidget(self.text_edit, 1, 0, 1, 2)

        self.btn_edit = FPushButton("编辑", self)
        self.glyt.addWidget(self.btn_edit, 2, 0, 1, 2)


if __name__ == "__main__":
    app = QApplication()
    text_edit = TestEdit()
    text_edit.show()
    app.exec()
