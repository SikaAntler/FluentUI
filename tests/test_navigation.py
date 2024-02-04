from functools import partial
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QWidget,
    QFrame,
)

from fluentui.utils import FIcon, set_font
from fluentui.framesless import FramelessMainWindow
from fluentui.widgets import (
    NavigationInterface,
    NavigationPanel,
    NavigationPushButton,
    NavigationToolButton,
    PanelPosition,
)


class TestPanel(FramelessMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Test Navigation Panel")
        self.resize(1187, 667)

        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        self.hlyt = QHBoxLayout(self.widget_central)
        self.hlyt.setContentsMargins(4, 4, 0, 0)
        # self.hlyt.setSpacing(0)

        self.btn_menu = NavigationToolButton(FIcon.LINE_HORIZONTAL_3)
        self.btn_menu.clicked.connect(self.on_btn_menu_clicked)
        self.hlyt.addWidget(self.btn_menu, 0, Qt.AlignmentFlag.AlignTop)

        self.navigation_panel = NavigationPanel(self, True)
        self.navigation_panel.move(0, 31)
        # self.navigation_panel.setMenuButtonVisible(True)
        self.navigation_panel.hide()

        self.nw_search = NavigationPushButton(FIcon.SEARCH, "搜索")
        self.nw_search.clicked.connect(self.on_nw_search_clicked)
        self.navigation_panel.addWidget(self.nw_search)

        self.lbl_main = QLabel("主界面")
        set_font(self.lbl_main, font_size=24)
        self.hlyt.addWidget(self.lbl_main, 1, Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(
            """
            TestPanel {
                background-color: rgb(249, 249, 249);
            }
            """
        )

    def on_btn_menu_clicked(self) -> None:
        self.navigation_panel.show()
        # self.navigation_panel.raise_()
        self.navigation_panel.expand()

    def on_nw_search_clicked(self) -> None:
        self.nw_search.setSelected(True)
        print("I am search")


class InterfaceWidget(QFrame):
    def __init__(self, text: str, parent=None) -> None:
        super().__init__(parent=parent)

        self.hlyt = QHBoxLayout(self)
        self.lbl = QLabel(text, self)
        self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hlyt.addWidget(self.lbl, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(" ", "_"))
        set_font(self.lbl, font_size=40)


class TestInterface(FramelessMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Test Navigation Interface")
        self.resize(1187, 667)

        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)

        self.hlyt = QHBoxLayout(self.widget_central)
        self.hlyt.setContentsMargins(0, 0, 0, 0)
        self.hlyt.setSpacing(0)
        # self.widget_central.setLayout(self.hlyt)

        self.navigation = NavigationInterface(self)
        # self.navigation.raise_()
        self.hlyt.addWidget(self.navigation)
        self.widget_stack = QStackedWidget(self)
        self.hlyt.addWidget(self.widget_stack, 1)

        self.interface_search = InterfaceWidget("搜索页面", self)
        self.add_interface(
            self.interface_search, FIcon.SEARCH, self.interface_search.objectName()
        )

        self.interface_image = InterfaceWidget("图像页面", self)
        self.add_interface(
            self.interface_image, FIcon.IMAGE, self.interface_image.objectName()
        )

        self.widget_stack.currentChanged.connect(self.on_widget_stack_currentChanged)
        self.widget_stack.setCurrentWidget(self.interface_search)
        self.navigation.setCurrentItem(self.interface_search.objectName())

        self.setStyleSheet(
            """
            InterfaceWidget {
                background-color: rgb(249, 249, 249);
                border: 1px solid rgb(229, 229, 229);
                border-right: none;
                border-bottom: none;
                border-top-left-radius: 10px;
            }
            TestInterface {
                background-color: rgb(243, 243, 243);
            }
            """
        )

    def add_interface(self, interface: QWidget, icon: FIcon, text: str) -> None:
        self.navigation.addItem(icon, text, lambda: self.switch_interface(interface))
        self.widget_stack.addWidget(interface)

    def switch_interface(self, interface: QWidget) -> None:
        self.widget_stack.setCurrentWidget(interface)

    def on_widget_stack_currentChanged(self, index: int) -> None:
        interface = self.widget_stack.widget(index)
        self.navigation.setCurrentItem(interface.objectName())


if __name__ == "__main__":
    app = QApplication()

    # panel = TestPanel()
    # panel.show()

    win = TestInterface()
    win.show()

    app.exec()
