from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QWidget

from fluentui.utils import FIcon, set_font
from fluentui.widgets import (
    FMainWindow,
    NavigationPanel,
    NavigationPushButton,
    NavigationToolButton,
    PanelPosition,
)


class MainWindow(FMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test Navigation Panel")
        self.resize(1187, 667)

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        self.hlyt = QHBoxLayout()
        self.hlyt.setContentsMargins(4, 4, 0, 0)
        # self.hlyt.setSpacing(0)
        self.widget_central.setLayout(self.hlyt)

        self.btn_menu = NavigationToolButton(FIcon.LINE_HORIZONTAL_3)
        self.btn_menu.clicked.connect(self.on_btn_menu_clicked)
        self.hlyt.addWidget(self.btn_menu, 0, Qt.AlignmentFlag.AlignTop)

        self.navigation_panel = NavigationPanel(self)
        self.navigation_panel.move(0, 31)
        # self.navigation_panel.setMenuButtonVisible(True)
        self.navigation_panel.hide()

        self.nw_search = NavigationPushButton(FIcon.SEARCH, "搜索")
        self.nw_search.clicked.connect(self.on_nw_search_clicked)
        self.navigation_panel.addWidget(self.nw_search, PanelPosition.TOP)

        self.lbl_main = QLabel("主界面")
        set_font(self.lbl_main, font_size=24)
        self.hlyt.addWidget(self.lbl_main, 1, Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(
            """
        MainWindow {
            background-color: rgb(249, 249, 249);
        }
        """
        )

    def on_btn_menu_clicked(self):
        self.navigation_panel.show()
        # self.navigation_panel.raise_()
        self.navigation_panel.expand()

    def on_nw_search_clicked(self):
        self.nw_search.setSelected(True)
        print("I am search")


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
