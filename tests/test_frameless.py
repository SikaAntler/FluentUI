from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from fluentui.framesless import (
    FramelessDialog,
    FramelessMainWindow,
    FramelessWidget,
)


class Widget(FramelessWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.update_frameless()

        self.title_bar.setDoubleClickedEnabled(False)

        # self.setAttribute(Qt.WidgetAttribute.WA_QuitOnClose)

        self.setWindowTitle("Frameless Widget")
        self.resize(400, 300)

        self.title_bar.btn_close.clicked.disconnect(self.close)
        self.title_bar.btn_close.clicked.connect(self.hide)


class Dialog(FramelessDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setWindowTitle("Frameless Dialog")
        self.resize(400, 300)

        # self.title_bar.btn_close.clicked.disconnect(self.close)

        self.vlyt = QVBoxLayout(self)

        self.btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.vlyt.addWidget(self.btn_box)


class MainWindow(FramelessMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setWindowTitle("Frameless Main Window")
        self.resize(1187, 667)

        self.widget_central = QWidget(self)
        self.widget_central.setMouseTracking(True)
        self.setCentralWidget(self.widget_central)
        self.hlyt = QHBoxLayout(self.widget_central)

        self.frameless_widget = Widget(self)

        self.btn_show_widget = QPushButton("Frameless Widget", self)
        self.hlyt.addWidget(self.btn_show_widget)
        self.btn_show_widget.clicked.connect(self.on_btn_show_widget_clicked)

        self.frameless_dialog = Dialog(self)

        self.btn_show_dialog = QPushButton("Frameless Dialog", self)
        self.hlyt.addWidget(self.btn_show_dialog)
        self.btn_show_dialog.clicked.connect(self.on_btn_show_dialog_clicked)

    def on_btn_show_widget_clicked(self) -> None:
        self.frameless_widget.setVisible(not self.frameless_widget.isVisible())

    def on_btn_show_dialog_clicked(self) -> None:
        dialog_code = self.frameless_dialog.exec()
        if dialog_code == QDialog.DialogCode.Accepted:
            print("Accepted")
        else:
            print("Rejected")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.frameless_widget.close()


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
