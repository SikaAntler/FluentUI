from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSlider,
    QWidget,
)

from fluentui.utils import set_font
from fluentui.widgets import FSlider


class TestSlider(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test Slider")
        self.resize(400, 300)

        self.widget_main = QWidget()
        self.setCentralWidget(self.widget_main)

        self.glyt_main = QGridLayout(self.widget_main)

        self.h_qslider = QSlider(Qt.Orientation.Horizontal)
        self.h_qslider.setTickInterval(5)
        self.h_qslider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.glyt_main.addWidget(self.h_qslider, 0, 0)

        self.v_qslider = QSlider(Qt.Orientation.Vertical)
        self.glyt_main.addWidget(self.v_qslider, 0, 1)

        self.v_fslider = FSlider(Qt.Orientation.Vertical)
        self.glyt_main.addWidget(self.v_fslider, 1, 0)

        self.h_fslider = FSlider(Qt.Orientation.Horizontal)
        self.h_fslider.setSingleStep(10)
        self.glyt_main.addWidget(self.h_fslider, 1, 1)


class TestSliderWithValue(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test Slider with Value")
        self.resize(300, 100)

        self.widget_main = QWidget()
        self.setCentralWidget(self.widget_main)

        self.hlyt_main = QHBoxLayout(self.widget_main)
        self.hlyt_main.setSpacing(0)

        self.slider = FSlider(Qt.Orientation.Horizontal)
        print(self.slider.singleStep(), self.slider.pageStep())
        self.slider.setSingleStep(1)
        self.slider.setPageStep(5)
        self.hlyt_main.addWidget(self.slider, 11)

        self.lbl_value = QLabel(str(self.slider.minimum()))
        set_font(self.lbl_value, font_size=12)
        self.hlyt_main.addWidget(self.lbl_value, 1, Qt.AlignmentFlag.AlignCenter)

        self.slider.valueChanged.connect(self.on_slider_valueChange)

    def on_slider_valueChange(self):
        value = self.slider.value()
        print(value)
        self.lbl_value.setText(str(value))


if __name__ == "__main__":
    app = QApplication()
    win0 = TestSlider()
    win0.show()
    win1 = TestSliderWithValue()
    win1.show()
    app.exec()
