from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from fluentui.widgets import FSwitchButton, IndicatorPosition


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(400, 300)

        self.widget_main = QWidget()
        self.vlyt_main = QVBoxLayout(self.widget_main)
        self.setCentralWidget(self.widget_main)

        self.switch_button = FSwitchButton()
        self.vlyt_main.addWidget(self.switch_button)

        self.switch_button_left = FSwitchButton(IndicatorPosition.LEFT)
        self.vlyt_main.addWidget(self.switch_button_left)

        self.switch_button_right = FSwitchButton(IndicatorPosition.RIGHT)
        self.switch_button_right.setEnabled(False)
        self.vlyt_main.addWidget(self.switch_button_right)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
