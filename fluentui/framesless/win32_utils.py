from ctypes import POINTER, Structure, c_int, windll
from ctypes.wintypes import HWND, RECT, UINT

import win32con
import win32gui

from ..utils import get_screen_geometry


class PWINDOWPOS(Structure):
    _fields_ = [
        ("hWnd", HWND),
        ("hwndInsertAfter", HWND),
        ("x", c_int),
        ("y", c_int),
        ("cx", c_int),
        ("cy", c_int),
        ("flags", UINT),
    ]


class NCCALCSIZE_PARAMS(Structure):
    _fields_ = [
        # ("rgrc", RECT * 3),  # TODO: 为什么要乘3
        ("rgrc", RECT),
        ("lppos", POINTER(PWINDOWPOS)),
    ]


LPNCCALCSIZE_PARAMS = POINTER(NCCALCSIZE_PARAMS)


def is_maximized(hWnd: int) -> bool:
    placement = win32gui.GetWindowPlacement(hWnd)

    return placement[1] == win32con.SW_MAXIMIZE


def is_fullscreen(hWnd: int) -> bool:
    rect = win32gui.GetWindowRect(hWnd)  # (left, top, right, bottom)
    geo = get_screen_geometry(available=False)
    screen = (geo.left(), geo.top(), geo.right(), geo.bottom())

    return all(i == j for i, j in zip(rect, screen))


def get_system_metrics(hWnd: int, index: int) -> int:
    dpi = windll.user32.GetDpiForWindow(hWnd)
    metrics = windll.user32.GetSystemMetricsForDpi(index, dpi)

    return metrics


def get_resize_border_thickness(hWnd: int, horizontal: bool):
    frame = win32con.SM_CXSIZEFRAME if horizontal else win32con.SM_CYSIZEFRAME
    thickness_0 = get_system_metrics(hWnd, frame)
    thickness_1 = get_system_metrics(hWnd, 92)

    return thickness_0 + thickness_1
