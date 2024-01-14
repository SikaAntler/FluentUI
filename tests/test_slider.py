from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QSlider,
    QWidget,
)

from fluentui.widgets import FSlider


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(400, 300)

        self.widget_main = QWidget()
        self.glyt_main = QGridLayout(self.widget_main)
        self.setCentralWidget(self.widget_main)

        self.h_qslider = QSlider(Qt.Orientation.Horizontal)
        self.glyt_main.addWidget(self.h_qslider, 0, 0)

        self.v_qslider = QSlider(Qt.Orientation.Vertical)
        self.glyt_main.addWidget(self.v_qslider, 0, 1)

        self.v_fslider = FSlider(Qt.Orientation.Vertical)
        self.glyt_main.addWidget(self.v_fslider, 1, 0)

        self.h_fslider = FSlider(Qt.Orientation.Horizontal)
        print(self.h_fslider.minimum(), self.h_fslider.maximum())
        self.glyt_main.addWidget(self.h_fslider, 1, 1)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
