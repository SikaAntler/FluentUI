from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent, QResizeEvent
from PySide6.QtWidgets import QDialog, QMainWindow, QWidget

from .title_bar import TitleBar


# class FramelessHelper(QMainWindow):  # PySide6多继承有bug
class FramelessHelper:
    BORDER = 5

    def __init__(self, parent=None) -> None:
        super().__init__()

        self.setMouseTracking(True)

        self.title_bar = TitleBar(self)

        self._resize_edge = None

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self.isMaximized():
            x, y = event.position().toTuple()
            is_top = y < self.BORDER
            is_left = x < self.BORDER
            is_right = self.width() - self.BORDER < x
            is_bottom = self.height() - self.BORDER < y

            if is_left and is_top:  # 左上
                cursor = Qt.CursorShape.SizeFDiagCursor
                edge = Qt.Edge.LeftEdge | Qt.Edge.TopEdge
            elif is_right and is_top:  # 右上
                cursor = Qt.CursorShape.SizeBDiagCursor
                edge = Qt.Edge.RightEdge | Qt.Edge.TopEdge
            elif is_right and is_bottom:  # 右下
                cursor = Qt.CursorShape.SizeFDiagCursor
                edge = Qt.Edge.RightEdge | Qt.Edge.BottomEdge
            elif is_left and is_bottom:  # 左下
                cursor = Qt.CursorShape.SizeBDiagCursor
                edge = Qt.Edge.LeftEdge | Qt.Edge.BottomEdge
            elif is_top:
                cursor = Qt.CursorShape.SizeVerCursor
                edge = Qt.Edge.TopEdge
            elif is_left:
                cursor = Qt.CursorShape.SizeHorCursor
                edge = Qt.Edge.LeftEdge
            elif is_right:
                cursor = Qt.CursorShape.SizeHorCursor
                edge = Qt.Edge.RightEdge
            elif is_bottom:
                cursor = Qt.CursorShape.SizeVerCursor
                edge = Qt.Edge.BottomEdge
            else:
                cursor = Qt.CursorShape.ArrowCursor
                edge = None

            self.setCursor(cursor)
            self._resize_edge = edge

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self._resize_edge is not None:
                self.windowHandle().startSystemResize(self._resize_edge)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.title_bar.resize(self.width(), self.title_bar.height())

    def update_frameless(self) -> None:
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            # | Qt.WindowType.WindowSystemMenuHint
            | Qt.WindowType.WindowMinimizeButtonHint
        )


class WindowsFrameDialog(FramelessHelper, QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.update_frameless()

        self.title_bar.btn_minimize.hide()
        self.title_bar.btn_maximize.hide()


class WindowsFramelessMainWindow(FramelessHelper, QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.update_frameless()

        self.setMenuWidget(self.title_bar)


class WindowsFramesWidget(FramelessHelper, QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.update_frameless()
