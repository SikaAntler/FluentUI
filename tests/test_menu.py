from PySide6.QtGui import QAction, QContextMenuEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu

from fluentui.utils import FIcon
from fluentui.widgets import FMenu, MenuAnimationType


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fluent Menu")
        self.resize(1187, 667)

        # self.menu = QMenu(self)
        self.menu = FMenu(self)

        self.action_add = QAction(FIcon.ADD.icon(), "新建")
        self.menu.addAction(self.action_add)

        self.action_delete = QAction(FIcon.DELETE.icon(), "删除")
        self.menu.addAction(self.action_delete)

        self.action_folder_open = QAction(FIcon.FOLDER_OPEN.icon(), "打开文件夹")
        self.menu.addAction(self.action_folder_open)

        self.menu.addSeparator()

        self.action_settings = QAction(FIcon.SETTINGS.icon(), "设置")
        self.menu.addAction(self.action_settings)

        # signals and slots
        self.action_add.triggered.connect(self.on_action_add_triggered)

    def contextMenuEvent(self, event: QContextMenuEvent):
        self.menu.exec(event.globalPos(), MenuAnimationType.DROP_DOWN)

    def on_action_add_triggered(self):
        print("Action add triggered")


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
