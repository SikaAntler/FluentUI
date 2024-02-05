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
    font_size: int = 14,
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

    font = QFont(families, font_size, weight, italic)
    # font.setFamilies(families)
    # font.setPixelSize(14)
    # font.setWeight(weight)
    # font.setItalic(italic)

    return font


def set_font(
    widget: QWidget,
    mono: bool = False,
    font_size: int = 12,
    weight: QFont.Weight = QFont.Weight.Normal,
    italic: bool = False,
) -> None:
    widget.setFont(get_font(mono, font_size, weight, italic))
