from PySide6.QtCore import QRect
from PySide6.QtWidgets import QApplication, QWidget


def get_screen_geometry(available=True) -> QRect:
    screen = QApplication.primaryScreen()

    return screen.availableGeometry() if available else screen.geometry()


def move_to_screen_center(widget: QWidget) -> None:
    # 需要用available...会把系统的菜单栏去掉
    if widget.isMaximized() or widget.isFullScreen():
        return

    geometry = get_screen_geometry()
    x = (geometry.width() - widget.width()) // 2
    y = (geometry.height() - widget.height()) // 2
    widget.move(x, y)
