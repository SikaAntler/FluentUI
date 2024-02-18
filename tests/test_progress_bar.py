from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QProgressBar, QVBoxLayout, QWidget

from fluentui.utils import FluentColor
from fluentui.widgets import (
    FMainWindow,
    FProgressBar,
    FPushButton,
    IndeterminateProgressBar,
)


class MainWindow(FMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.resize(400, 400)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.vlyt = QVBoxLayout(self.widget)

        self.progress_qt = QProgressBar(self)
        self.progress_qt.setRange(0, 100)
        self.vlyt.addWidget(self.progress_qt)

        self.progress_fluent = FProgressBar(self)
        self.progress_fluent.setRange(0, 100)
        self.progress_fluent.setBarColor(FluentColor.GOLD.color())
        self.vlyt.addWidget(self.progress_fluent)

        self.progress_indeterminate = IndeterminateProgressBar(self)
        self.progress_indeterminate.setBarColor(FluentColor.YELLOW_GOLD.color())
        self.vlyt.addWidget(self.progress_indeterminate)

        self.btn_start = FPushButton("开始")
        self.vlyt.addWidget(self.btn_start)

        self.timer_qt = QTimer(self)
        self.timer_qt.setInterval(100)

        self.timer_fluent = QTimer(self)
        self.timer_fluent.setInterval(100 * 20)

        self.btn_start.clicked.connect(self.on_btn_start_clicked)
        self.timer_qt.timeout.connect(self.on_timer_qt_timeout)
        self.timer_fluent.timeout.connect(self.on_timer_fluent_timeout)

    def on_timer_qt_timeout(self) -> None:
        value = self.progress_qt.value() + 1
        self.progress_qt.setValue(value)

    def on_timer_fluent_timeout(self) -> None:
        value = self.progress_fluent.value() + 20
        self.progress_fluent.setValue(value)

    def on_btn_start_clicked(self) -> None:
        if self.btn_start.text() == "开始":
            self.timer_qt.start()
            self.timer_fluent.start()
            self.progress_indeterminate.start()
            self.btn_start.setText("暂停")
        else:
            self.timer_qt.stop()
            self.timer_fluent.stop()
            self.progress_indeterminate.pause()
            self.btn_start.setText("开始")


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()
    win.show()
    app.exec()
