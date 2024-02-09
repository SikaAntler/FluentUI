from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QScrollArea, QVBoxLayout, QWidget

from fluentui.utils import FIcon
from fluentui.widgets import (
    FSmoothScrollBar,
    IndicatorPosition,
    PushSettingCard,
    SettingCardGroup,
    SliderSettingCard,
    SwitchSettingCard,
)


class Settings(QScrollArea):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setWindowTitle("Test Setting Card")
        self.resize(400, 400)

        self.scroll_bar_v = FSmoothScrollBar(Qt.Orientation.Vertical, self)
        self.scroll_bar_v.setScrollRate(60)
        self.scroll_bar_h = FSmoothScrollBar(Qt.Orientation.Horizontal, self)

        self.widget_scroll = QWidget()
        self.setWidget(self.widget_scroll)
        self.setWidgetResizable(True)
        self.setViewportMargins(20, 20, 20, 20)

        self.vlyt = QVBoxLayout(self.widget_scroll)
        self.vlyt.setContentsMargins(0, 0, 0, 0)
        self.vlyt.setSpacing(28)

        self.group_image = SettingCardGroup("图像", self.widget_scroll)
        self.vlyt.addWidget(self.group_image)

        content = Path(__file__).parent / "images"
        self.card_select_folder = PushSettingCard(
            "选择文件夹", FIcon.FOLDER, "图像文件夹", str(content)
        )
        self.group_image.addSettingCard(self.card_select_folder)

        self.group_auto = SettingCardGroup("启动项", self.widget_scroll)
        self.vlyt.addWidget(self.group_auto)

        self.card_auto_open_camera = SwitchSettingCard(
            IndicatorPosition.RIGHT, FIcon.CAMERA, "自动开启相机"
        )
        self.group_auto.addSettingCard(self.card_auto_open_camera)

        self.card_auto_open_serial = SwitchSettingCard(
            IndicatorPosition.RIGHT, FIcon.SERIAL_PORT, "自动开启串口"
        )
        self.group_auto.addSettingCard(self.card_auto_open_serial)

        self.group_draw_label = SettingCardGroup("标签", self.widget_scroll)
        self.vlyt.addWidget(self.group_draw_label)

        self.card_draw_label = SwitchSettingCard(
            IndicatorPosition.RIGHT, FIcon.TEXT, "绘制标签"
        )
        self.group_draw_label.addSettingCard(self.card_draw_label)

        self.card_draw_label_size = SliderSettingCard(FIcon.DRAW_TEXT, "绘制字体大小")
        self.card_draw_label_size.slider.setFixedWidth(150)
        self.group_draw_label.addSettingCard(self.card_draw_label_size)

        self.card_select_folder.clicked.connect(self.on_card_select_folder_clicked)
        self.card_auto_open_camera.checkedChanged.connect(
            self.on_card_auto_open_camera_checkedChanged
        )
        self.card_draw_label_size.valueChanged.connect(
            self.on_card_draw_label_size_valueChanged
        )

        self.vlyt.addStretch(1)

    def on_card_select_folder_clicked(self) -> None:
        print(self.card_select_folder.content())

    def on_card_auto_open_camera_checkedChanged(self) -> None:
        print(self.card_auto_open_camera.isChecked())

    def on_card_draw_label_size_valueChanged(self) -> None:
        print(self.card_draw_label_size.value())


if __name__ == "__main__":
    app = QApplication()
    win = Settings()
    win.show()
    app.exec()
