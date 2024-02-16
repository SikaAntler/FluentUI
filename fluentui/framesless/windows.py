from ctypes import cast
from ctypes.wintypes import LPRECT, MSG

import win32con
import win32gui
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QResizeEvent
from PySide6.QtWidgets import QDialog, QMainWindow, QWidget

from .title_bar import TitleBar
from .win32_utils import (
    LPNCCALCSIZE_PARAMS,
    get_resize_border_thickness,
    is_fullscreen,
    is_maximized,
)


# class FramelessHelper(QMainWindow):  # PySide6多继承有bug
class FramelessHelper:
    BORDER = 7

    def __init__(self, parent) -> None:
        super().__init__()

        self.title_bar = TitleBar(self)
        # self.title_bar.installEventFilter(self)

        self._enable_resize = True

    def add_window_animation(self) -> None:
        style = win32gui.GetWindowLong(self.winId(), win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            self.winId(),
            win32con.GWL_STYLE,
            style
            | win32con.WS_MINIMIZEBOX
            | win32con.WS_MAXIMIZEBOX
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME
            | win32con.WS_CAPTION,
        )

    def update_frameless(self) -> None:
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.add_window_animation()

    def nativeEvent(self, eventType, message: int) -> tuple[bool, int]:
        msg = MSG.from_address(int(message))
        if not msg.hWnd:
            print("not msg.hWnd")
            return False, 0

        if msg.message == win32con.WM_NCHITTEST and self._enable_resize:
            pos = QCursor.pos()
            # 因为FramelessWindowHint，geometry和frameGeometry相等
            x, y = pos.x() - self.x(), pos.y() - self.y()

            is_left = x < self.BORDER
            is_top = y < self.BORDER
            is_right = self.width() - self.BORDER < x
            is_bottom = self.height() - self.BORDER < y

            if is_left and is_top:  # 左上
                return True, win32con.HTTOPLEFT
            elif is_right and is_top:  # 右上
                return True, win32con.HTTOPRIGHT
            elif is_right and is_bottom:  # 右下
                return True, win32con.HTBOTTOMRIGHT
            elif is_left and is_bottom:  # 左下
                return True, win32con.HTBOTTOMLEFT
            elif is_left:
                return True, win32con.HTLEFT
            elif is_top:
                return True, win32con.HTTOP
            elif is_right:
                return True, win32con.HTRIGHT
            elif is_bottom:
                return True, win32con.HTBORDER

        elif msg.message == win32con.WM_NCCALCSIZE:
            if msg.wParam:
                # rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
                rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc
            else:
                print("not msg.wParam")
                rect = cast(msg.lParam, LPRECT)

            # ⚠如果是调用Qt自带的showMaximized()，可以用isMaximized()判断
            # 然而如果是拖拽通过系统触发，此时是不能用isMaximized()判断的
            is_max = is_maximized(msg.hWnd)
            is_full = is_fullscreen(msg.hWnd)

            if is_max and not is_full:
                tx = get_resize_border_thickness(self.winId(), horizontal=True)
                rect.left += tx
                rect.right -= tx

                ty = get_resize_border_thickness(self.winId(), horizontal=False)
                rect.top += ty
                rect.bottom -= ty

            return True, 0 if not msg.wParam else win32con.WVR_REDRAW

        return False, 0

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.title_bar.resize(self.width(), self.title_bar.height())

        super().resizeEvent(event)


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

        self.setContentsMargins(0, 32, 0, 0)
