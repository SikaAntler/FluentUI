from enum import Enum
from platform import system

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget


class FFont:
    class Serif(Enum):
        MACOS = ["SF Pro", "PingFang SC"]
        WINDOWS = ["Segoe UI", "Microsoft YaHei"]

    class Mono(Enum):
        MACOS = ["SF Mono", "Menlo"]
        WINDOWS = ["Consolas"]


def get_font(
    mono: bool = False,
    font_size: float = 12,
    weight: QFont.Weight = QFont.Weight.Normal,
    italic: bool = False,
) -> QFont:
    os = system()
    if os == "Darwin":
        families = []
        if mono:
            families.extend(FFont.Mono.MACOS.value)
        families.extend(FFont.Serif.MACOS.value)
    elif os == "Windows":
        families = []
        if mono:
            families.extend(FFont.Mono.WINDOWS.value)
        families.extend(FFont.Serif.WINDOWS.value)
    else:
        raise ValueError("Unknown operating system")

    font = QFont(families, weight=weight, italic=italic)
    font.setPointSizeF(font_size)

    return font


def set_font(
    widget: QWidget,
    mono: bool = False,
    font_size: float = 10.5,
    weight: QFont.Weight = QFont.Weight.Normal,
    italic: bool = False,
) -> None:
    """设置字体

    P.S. 为了适配不同缩放比例，选择pointSizeF来表示字体大小
    pointSize->pixelSize计算公式为：pointSize * 96 / 72 = pixelSize
    为了使最终字体笔画匀称，应确保pixelSize的值为整数，一下使是常用的pointSizeF值：
    9 -> 12px, 10.5 -> 14px, 12 -> 16px, 13.5 -> 18px, 15 -> 20px

    """

    widget.setFont(get_font(mono, font_size, weight, italic))
