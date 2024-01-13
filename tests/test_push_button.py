from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QWidget,
)

from fluentui.utils import FluentIcon
from fluentui.widgets import FPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(400, 300)

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.glyt_main = QGridLayout(self.widget_central)

        self.button_add = QPushButton(FluentIcon.ADD.icon(), "新建")
        self.glyt_main.addWidget(self.button_add, 0, 0)

        self.button_delete = FPushButton(FluentIcon.DELETE.icon(), "删除")
        self.glyt_main.addWidget(self.button_delete, 0, 1)

        self.button_last = FPushButton(FluentIcon.ARROW_CIRCLE_UP.icon(), "上一个")
        self.button_last.setEnabled(False)
        self.glyt_main.addWidget(self.button_last, 1, 0)

        self.button_next = FPushButton(text="下一个")
        self.glyt_main.addWidget(self.button_next, 1, 1)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
