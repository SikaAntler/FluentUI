from PySide6.QtGui import QContextMenuEvent
from PySide6.QtWidgets import QApplication, QMainWindow

from fluentui.utils import FAction, FIcon
from fluentui.widgets import FMenu, MenuAnimationType


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fluent Menu")
        self.resize(1187, 667)

        self.menu = FMenu(self)

        self.action_edit_label = FAction(FIcon.EDIT, "标注")
        self.action_edit_label.setShortcut("Y")
        self.menu.addAction(self.action_edit_label)

        self.action_retrieval = FAction(FIcon.IMAGE_SEARCH, "推荐")
        self.action_retrieval.setShortcut("R")
        self.menu.addAction(self.action_retrieval)

        self.menu.addSeparator()

        self.action_fit_edges = FAction(FIcon.CROP, "贴合")
        self.action_fit_edges.setShortcut("F")
        self.menu.addAction(self.action_fit_edges)

        self.action_remove_bbox = FAction(FIcon.DELETE, "删除")
        self.action_remove_bbox.setShortcut("Ctrl+D")
        self.menu.addAction(self.action_remove_bbox)

        # signals and slots
        self.action_edit_label.triggered.connect(self.on_action_edit_label_triggered)

    def contextMenuEvent(self, event: QContextMenuEvent):
        self.menu.exec(event.globalPos(), MenuAnimationType.DROP_DOWN)

    def on_action_edit_label_triggered(self):
        print("Action edit label triggered")


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
