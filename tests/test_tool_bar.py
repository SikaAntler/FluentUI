from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QToolBar,
    QWidget,
)

from fluentui.utils import FluentIcon
from fluentui.widgets import FToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fluent Tool Bar")
        self.resize(1187, 667)

        self.widget_central = QWidget()
        self.glyt_main = QGridLayout(self.widget_central)
        self.setCentralWidget(self.widget_central)

        # self.tool_bar = QToolBar()
        # self.addToolBar(self.tool_bar)
        self.tool_bar = FToolBar()
        self.glyt_main.addWidget(self.tool_bar, 0, 0)

        self.action_image = QAction(FluentIcon.IMAGE.icon(), "打开图像")
        self.tool_bar.addAction(self.action_image)

        self.action_folder_open = QAction(FluentIcon.FOLDER_OPEN.icon(), "打开文件夹")
        self.tool_bar.addAction(self.action_folder_open)

        self.tool_bar.addSeparator()

        self.action_last = QAction(FluentIcon.ARROW_CIRCLE_UP.icon(), "上一个")
        self.tool_bar.addAction(self.action_last)

        self.action_next = QAction(FluentIcon.ARROW_CIRCLE_DOWN.icon(), "下一个")
        self.tool_bar.addAction(self.action_next)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
