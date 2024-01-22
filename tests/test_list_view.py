from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QListWidgetItem,
    QMainWindow,
    QWidget,
)

from fluentui.widgets import FListWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(300, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.hlyt = QHBoxLayout(self.central_widget)

        self.list_widget = FListWidget()
        self.hlyt.addWidget(self.list_widget)

        data = [
            "裸藻属",
            "鼓藻属",
            "扁裸藻属",
            "新月藻属",
            "盘星藻属",
            "栅藻属",
            "小环藻属",
            "舟型藻属",
            "微囊藻属",
            "直链藻属",
            "异极藻属",
            "四角藻属",
            "纤维藻属",
            "双菱藻属",
            "空星藻属",
            "脆杆藻属",
            "十字藻属",
            "鱼腥藻属",
            "月牙藻属",
            "丝藻属",
            "卵囊藻属",
            "颤藻属",
            "弓形藻属",
            "束丝藻属",
            "隐藻属",
            "小球藻属",
            "角甲藻属",
            "螺旋藻属",
            "拟新月藻属",
        ]
        for item in data:
            self.list_widget.addItem(QListWidgetItem(item))

        self.setStyleSheet("MainWindow {background: rgb(243, 243, 243);}")


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
