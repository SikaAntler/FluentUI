from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QWidget


def move_to_screen_center(widget: QWidget) -> None:
    # MacOS在resize后就不居中了，后来发现在windows上也不会居中了
    # 需要用available...会把系统的菜单栏去掉，但Size和Geometry的区别还不清楚
    desktop = QGuiApplication.primaryScreen().availableSize()
    x = (desktop.width() - widget.width()) // 2
    y = (desktop.height() - widget.height()) // 2
    widget.move(x, y)
