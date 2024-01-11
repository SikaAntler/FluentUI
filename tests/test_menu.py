from PySide6.QtGui import QAction, QContextMenuEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu

from fluentui.utils import FluentIcon
from fluentui.widgets import FMenu, MenuAnimationType


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fluent Menu")
        self.resize(1187, 667)

        # self.menu = QMenu(self)
        self.menu = FMenu(self)

        self.action_add = QAction(FluentIcon.ADD.icon(), "新建")
        self.menu.addAction(self.action_add)

        self.action_delete = QAction(FluentIcon.DELETE.icon(), "删除")
        self.menu.addAction(self.action_delete)

        self.action_folder_open = QAction(FluentIcon.FOLDER_OPEN.icon(), "打开文件夹")
        self.menu.addAction(self.action_folder_open)

        self.menu.addSeparator()

        self.action_settings = QAction(FluentIcon.SETTINGS.icon(), "设置")
        self.menu.addAction(self.action_settings)

    def contextMenuEvent(self, event: QContextMenuEvent):
        self.menu.exec(event.globalPos(), MenuAnimationType.DROP_DOWN)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
