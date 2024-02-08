from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QWidget,
)

from fluentui.utils import FIcon
from fluentui.widgets import FPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(400, 300)

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.glyt_main = QGridLayout(self.widget_central)

        self.button_add = QPushButton("新建", self, FIcon.ADD.icon())
        self.glyt_main.addWidget(self.button_add, 0, 0)

        self.button_delete = FPushButton("删除", self, FIcon.DELETE.icon())
        self.glyt_main.addWidget(self.button_delete, 0, 1)

        self.button_last = FPushButton("上一个", self, FIcon.ARROW_CIRCLE_UP)
        self.button_last.setEnabled(False)
        self.glyt_main.addWidget(self.button_last, 1, 0)

        self.button_next = FPushButton("下一个", self)
        self.glyt_main.addWidget(self.button_next, 1, 1)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
