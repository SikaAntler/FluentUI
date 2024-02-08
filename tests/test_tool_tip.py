from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget

from fluentui.utils import FAction, FIcon
from fluentui.widgets import (
    FPushButton,
    FToolBar,
    FToolTipFilter,
    ToolTipPosition,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fluent Tool Tip")
        self.resize(400, 300)

        self.widget_central = QWidget()
        self.glyt = QGridLayout(self.widget_central)
        self.glyt.setContentsMargins(8, 0, 8, 8)
        self.glyt.setSpacing(8)
        self.setCentralWidget(self.widget_central)

        self.tool_bar = FToolBar()
        self.tool_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setMenuWidget(self.tool_bar)

        self.action_image = FAction(FIcon.IMAGE, "图像")
        self.action_image.setToolTip("打开一张图像")
        self.tool_bar.addAction(self.action_image)

        self.action_folder_open = FAction(FIcon.FOLDER_OPEN, "文件夹")
        self.action_folder_open.setToolTip("选择文件夹")
        self.tool_bar.addAction(self.action_folder_open)

        self.btn_last = FPushButton(FIcon.ARROW_CIRCLE_UP.icon(), "上一张")
        self.btn_last.setToolTip("打开上一张图像")
        self.btn_last.installEventFilter(
            FToolTipFilter(self.btn_last, 500, ToolTipPosition.TOP)
        )
        self.glyt.addWidget(self.btn_last, 0, 0)

        self.btn_next = FPushButton(FIcon.ARROW_CIRCLE_DOWN.icon(), "下一张")
        self.btn_next.setToolTip("打开下一张图像")
        self.btn_next.setToolTipDuration(1000)
        self.btn_next.installEventFilter(FToolTipFilter(self.btn_next))
        self.glyt.addWidget(self.btn_next, 0, 1)

        self.btn_left = FPushButton(FIcon.ARROW_CIRCLE_LEFT.icon(), "左移")
        self.btn_left.setToolTip("视野向左移动50微米")
        self.btn_left.installEventFilter(
            FToolTipFilter(self.btn_left, 500, ToolTipPosition.LEFT)
        )
        self.glyt.addWidget(self.btn_left, 1, 0)

        self.btn_right = FPushButton(FIcon.ARROW_CIRCLE_RIGHT.icon(), "右移")
        self.btn_right.setToolTip("视野向右移动50微米")
        self.btn_right.installEventFilter(
            FToolTipFilter(self.btn_right, 500, ToolTipPosition.RIGHT)
        )
        self.glyt.addWidget(self.btn_right, 1, 1)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
