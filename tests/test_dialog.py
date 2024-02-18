from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QGridLayout,
    QMessageBox,
    QWidget,
)

from fluentui.framesless import FramelessMainWindow
from fluentui.utils import FIcon
from fluentui.widgets import FDialog, FMessageBox, FPushButton


class MainWindow(FramelessMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Test Dialog")
        self.resize(400, 300)

        self.widget_central = QWidget(self)
        self.setCentralWidget(self.widget_central)

        self.glyt = QGridLayout(self.widget_central)

        self.btn_dialog_qt = FPushButton("Qt对话框", self)
        self.glyt.addWidget(self.btn_dialog_qt, 0, 0)
        self.btn_dialog_qt.clicked.connect(self.on_btn_dialog_qt_clicked)

        self.btn_mb_qt = FPushButton("Qt消息框", self)
        self.glyt.addWidget(self.btn_mb_qt, 0, 1)
        self.btn_mb_qt.clicked.connect(self.on_btn_mb_qt_clicked)

        self.btn_dialog_fluent = FPushButton("Fluent对话框", self)
        self.glyt.addWidget(self.btn_dialog_fluent, 1, 0)
        self.btn_dialog_fluent.clicked.connect(self.on_btn_dialog_fluent_clicked)

        self.btn_mb_fluent = FPushButton("Fluent消息框", self)
        self.glyt.addWidget(self.btn_mb_fluent, 1, 1)
        self.btn_mb_fluent.clicked.connect(self.on_btn_mb_fluent_clicked)

        self.question_title = "询问"
        self.question_text = "是否要选择此项？"
        self.information_title = "提示"
        self.information_text = "设置已完成，请重启软件"
        self.warning_title = "警告"
        self.warning_text = "请检查设置！"
        self.critical_title = "错误"
        self.critical_text = "程序崩溃，软件即将退出"

    def on_btn_dialog_qt_clicked(self) -> None:
        dialog = QDialog(self)
        dialog.resize(300, 300)
        dialog.exec()
        if dialog.result() == QDialog.DialogCode.Accepted:
            print("Qt dialog accepted")
        else:
            print("Qt dialog rejected")

    def on_btn_mb_qt_clicked(self) -> None:
        QMessageBox.question(self, self.question_title, self.question_text)
        QMessageBox.information(self, self.information_title, self.information_text)
        box = QMessageBox(
            QMessageBox.Icon.Warning,
            self.question_title,
            self.question_text,
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel,
            self,
        )
        box.setWindowIcon(FIcon.WARNING.icon())
        box.exec()
        QMessageBox.critical(self, self.critical_title, self.critical_text)

    def on_btn_dialog_fluent_clicked(self) -> None:
        dialog = FDialog(self)
        dialog.resize(300, 300)
        dialog.exec()
        if dialog.result() == QDialog.DialogCode.Accepted:
            print("Qt dialog accepted")
        else:
            print("Qt dialog rejected")

    def on_btn_mb_fluent_clicked(self) -> None:
        FMessageBox.question(self, self.question_title, self.question_text)
        FMessageBox.information(self, self.information_title, self.information_text)
        box = FMessageBox(
            FIcon.WARNING,
            self.warning_title,
            self.warning_text,
            self,
            "#f78a4c",
        )
        box.exec()
        FMessageBox.critical(self, self.critical_title, self.critical_text)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
