from PySide6.QtCore import QEvent, QObject, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QDialog, QMainWindow, QWidget

from .title_bar import TitleBar


# class FramelessHelper(QMainWindow):  # PySide6多继承有bug
class FramelessHelper:
    BORDER = 5

    def __init__(self, parent=None) -> None:
        super().__init__()

        self.setMouseTracking(True)

        self._edge = None

        self.title_bar = TitleBar(self)
        self.title_bar.installEventFilter(self)

    def update_frameless(self) -> None:
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            # | Qt.WindowType.WindowSystemMenuHint
            | Qt.WindowType.WindowMinimizeButtonHint
        )

    def _determine_edge_cursor(self, pos: QPointF) -> None:
        x, y = pos.toTuple()
        is_top = y < self.BORDER
        is_left = x < self.BORDER
        is_right = self.width() - self.BORDER < x
        is_bottom = self.height() - self.BORDER < y

        if is_left and is_top:  # 左上
            edge = Qt.Edge.LeftEdge | Qt.Edge.TopEdge
            cursor = Qt.CursorShape.SizeFDiagCursor
        elif is_right and is_top:  # 右上
            edge = Qt.Edge.RightEdge | Qt.Edge.TopEdge
            cursor = Qt.CursorShape.SizeBDiagCursor
        elif is_right and is_bottom:  # 右下
            edge = Qt.Edge.RightEdge | Qt.Edge.BottomEdge
            cursor = Qt.CursorShape.SizeFDiagCursor
        elif is_left and is_bottom:  # 左下
            edge = Qt.Edge.LeftEdge | Qt.Edge.BottomEdge
            cursor = Qt.CursorShape.SizeBDiagCursor
        elif is_top:
            edge = Qt.Edge.TopEdge
            cursor = Qt.CursorShape.SizeVerCursor
        elif is_left:
            edge = Qt.Edge.LeftEdge
            cursor = Qt.CursorShape.SizeHorCursor
        elif is_right:
            edge = Qt.Edge.RightEdge
            cursor = Qt.CursorShape.SizeHorCursor
        elif is_bottom:
            edge = Qt.Edge.BottomEdge
            cursor = Qt.CursorShape.SizeVerCursor
        else:
            edge = None
            cursor = Qt.CursorShape.ArrowCursor

        self._edge = edge
        self.setCursor(cursor)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if not self.isMaximized():
            self._determine_edge_cursor(event.position())

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self._edge is not None:
                self.windowHandle().startSystemResize(self._edge)

        super().mousePressEvent(event)

    # def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         self._edge = None
    #         self.setCursor(Qt.CursorShape.ArrowCursor)
    #         # print(self._edge)
    #         # self._determine_edge_cursor(event.position())
    #
    #     super().mouseReleaseEvent(event)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched is self.title_bar and event.type() == QEvent.Type.MouseButtonPress:
            if self._edge is None:
                return False
            else:
                self.mousePressEvent(event)
                return True

        return super().eventFilter(watched, event)


class WindowsFrameDialog(FramelessHelper, QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.update_frameless()

        self.title_bar.btn_minimize.hide()
        self.title_bar.btn_maximize.hide()
        self.title_bar.setDoubleClickedEnabled(False)


class WindowsFramelessMainWindow(FramelessHelper, QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.update_frameless()

        self.setMenuWidget(self.title_bar)


class WindowsFramesWidget(FramelessHelper, QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.update_frameless()
