from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget

from fluentui.widgets import FLineEdit, FPushButton


class MainWindow(QMainWindow):
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


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
