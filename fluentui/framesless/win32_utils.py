from ctypes import POINTER, Structure, byref, c_int, windll
from ctypes.wintypes import HWND, RECT, UINT

import win32con
import win32gui

from ..utils import get_screen_geometry


def add_window_animation(hWnd: int) -> None:
    style = win32gui.GetWindowLong(hWnd, win32con.GWL_STYLE)
    win32gui.SetWindowLong(
        hWnd,
        win32con.GWL_STYLE,
        style
        | win32con.WS_MINIMIZEBOX
        | win32con.WS_MAXIMIZEBOX
        | win32con.CS_DBLCLKS
        | win32con.WS_THICKFRAME
        | win32con.WS_CAPTION,
    )


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


def dwm_is_composition_enabled() -> bool:
    b_result = c_int(0)
    windll.dwmapi.DwmIsCompositionEnabled(byref(b_result))

    return bool(b_result.value)


class MARGINS(Structure):
    _fields_ = [
        ("cxLeftWidth", c_int),
        ("cxRightWidth", c_int),
        ("cyToopHeight", c_int),
        ("cyBottomHeight", c_int),
    ]


def add_shadow_effect(hWnd: int) -> None:
    if not dwm_is_composition_enabled():
        print("DWM composition is disabled")
        return

    margins = MARGINS(-1, -1, -1, -1)
    windll.dwmapi.DwmExtendFrameIntoClientArea(hWnd, byref(margins))
