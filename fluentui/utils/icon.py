from enum import Enum

from PySide6.QtGui import QIcon


class FluentIcon(Enum):
    ADD = "add"
    ADD_CIRCLE = "add_circle"
    ADD_SQUARE = "add_square"
    ARROW_CIRCLE_DOWN = "arrow_circle_down"
    ARROW_CIRCLE_UP = "arrow_circle_up"
    CENTER_HORIZONTAL = "center_horizontal"
    DELETE = "delete"
    EDIT = "edit"
    FOLDER = "folder"
    FOLDER_OPEN = "folder_open"
    GROUP_LIST = "group_list"
    HOME = "home"
    IMAGE = "image"
    IMAGE_MULTIPLE = "image_multiple"
    LINE_HORIZONTAL_7 = "line_horizontal_3"
    OPEN_FOLDER = "open_folder"
    RENAME = "rename"
    SAVE = "save"
    SCALE_FIT = "scale_fit"
    SEARCH = "search"
    SETTINGS = "settings"
    SQUARE = "square"
    ZOOM_FIT = "zoom_fit"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"

    def icon(self) -> QIcon:
        path = f":/fluentui/{self.value}"
        return QIcon(path)
