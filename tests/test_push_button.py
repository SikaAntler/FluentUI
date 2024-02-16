from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QWidget,
)

from fluentui.utils import FIcon
from fluentui.widgets import FPushButton, PrimaryPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(400, 300)

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.glyt = QGridLayout(self.widget_central)

        self.btn_add = QPushButton("新建", self, FIcon.ADD.icon())
        self.glyt.addWidget(self.btn_add, 0, 0)

        self.btn_delete = FPushButton("删除", self, FIcon.DELETE.icon())
        self.glyt.addWidget(self.btn_delete, 0, 1)

        self.btn_last = FPushButton("上一个", self, FIcon.ARROW_CIRCLE_UP)
        self.btn_last.setEnabled(False)
        self.glyt.addWidget(self.btn_last, 1, 0)

        self.btn_next = FPushButton("下一个", self)
        self.glyt.addWidget(self.btn_next, 1, 1)

        self.btn_primary_last = PrimaryPushButton("上一个", self, FIcon.ARROW_CIRCLE_UP)
        self.btn_primary_last.setEnabled(False)
        self.glyt.addWidget(self.btn_primary_last)

        self.btn_primary_next = PrimaryPushButton(
            "下一个", self, FIcon.ARROW_CIRCLE_DOWN
        )
        self.glyt.addWidget(self.btn_primary_next)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
