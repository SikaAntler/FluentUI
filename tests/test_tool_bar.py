from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget

from fluentui.utils import FAction, FIcon
from fluentui.widgets import FToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fluent Tool Bar")
        self.resize(1187, 667)

        self.widget_central = QWidget()
        self.glyt_main = QGridLayout(self.widget_central)
        self.glyt_main.setContentsMargins(8, 0, 8, 8)
        self.glyt_main.setSpacing(8)
        self.setCentralWidget(self.widget_central)

        self.tool_bar = FToolBar()
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.glyt_main.addWidget(self.tool_bar, 0, 0)

        self.action_image = FAction(FIcon.IMAGE, "图像")
        self.action_image.setCheckable(True)
        self.tool_bar.addAction(self.action_image)
        # self.action_image.toggle()
        # self.action_image.setChecked(True)

        self.action_folder_open = FAction(FIcon.FOLDER_OPEN, "文件夹")
        self.action_folder_open.setCheckable(True)
        self.action_folder_open.setChecked(True)
        self.action_folder_open.setEnabled(False)
        self.tool_bar.addAction(self.action_folder_open)

        self.tool_bar.addSeparator()

        self.action_last = FAction(FIcon.ARROW_CIRCLE_UP.icon(), "上一个")
        self.tool_bar.addAction(self.action_last)

        self.action_next = FAction(FIcon.ARROW_CIRCLE_DOWN.icon(), "下一个")
        self.tool_bar.addAction(self.action_next)

        self.glyt_main.addWidget(QWidget())

        # signals and slots
        self.action_image.toggled.connect(self.on_action_image_toggled)

    def on_action_image_toggled(self):
        print(f"Action image toggled, isChecked={self.action_image.isChecked()}")


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
