from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QRadioButton,
    QWidget,
)

from fluentui.widgets import FRadioButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(400, 300)

        self.widget_main = QWidget()
        self.hlyt_main = QHBoxLayout(self.widget_main)
        self.setCentralWidget(self.widget_main)

        self.btn_0 = QRadioButton("选项一")
        self.btn_0.setChecked(True)
        self.hlyt_main.addWidget(self.btn_0)

        self.btn_1 = FRadioButton("选项二")
        self.hlyt_main.addWidget(self.btn_1)

        self.btn_2 = FRadioButton("选项三")
        self.hlyt_main.addWidget(self.btn_2)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
