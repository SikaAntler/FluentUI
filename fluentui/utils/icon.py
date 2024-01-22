from enum import Enum

from PySide6.QtCore import QFile, QRect, Qt
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtXml import QDomDocument


class FIcon(Enum):
    ADD = "add"
    ADD_CIRCLE = "add_circle"
    ADD_SQUARE = "add_square"
    ARROW_CIRCLE_DOWN = "arrow_circle_down"
    ARROW_CIRCLE_LEFT = "arrow_circle_left"
    ARROW_CIRCLE_RIGHT = "arrow_circle_right"
    ARROW_CIRCLE_UP = "arrow_circle_up"
    ARROW_DOWN = "arrow_down"
    ARROW_LEFT = "arrow_left"
    ARROW_RIGHT = "arrow_right"
    ARROW_UP = "arrow_up"
    CAMERA = "camera"
    CAMERA_EDIT = "camera_edit"
    CAMERA_OFF = "camera_off"
    CENTER_HORIZONTAL = "center_horizontal"
    DELETE = "delete"
    EDIT = "edit"
    FOLDER = "folder"
    FOLDER_OPEN = "folder_open"
    GROUP_LIST = "group_list"
    HOME = "home"
    IMAGE = "image"
    IMAGE_MULTIPLE = "image_multiple"
    LIGHTBULB = "lightbulb"
    LINE_HORIZONTAL_3 = "line_horizontal_3"
    OPEN_FOLDER = "open_folder"
    RENAME = "rename"
    SAVE = "save"
    SCALE_FIT = "scale_fit"
    SCAN_CAMERA = "scan_camera"
    SEARCH = "search"
    SERIAL_PORT = "serial_port"
    SETTINGS = "settings"
    SQUARE = "square"
    ZOOM_FIT = "zoom_fit"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"

    def icon(self) -> QIcon:
        return QIcon(self.path())

    def path(self) -> str:
        return f":/fluentui/{self.value}"

    def render(self, painter: QPainter, rect: QRect, state: QIcon.State) -> None:
        svg_file = QFile(self.path())
        svg_file.open(QFile.OpenModeFlag.ReadOnly)
        svg = svg_file.readAll()
        svg_file.close()

        if state == QIcon.State.On:
            dom = QDomDocument()
            dom.setContent(svg)
            node_list = dom.elementsByTagName("path")
            for i in range(node_list.length()):
                path_nodel = node_list.item(i)
                fill_node = path_nodel.attributes().namedItem("fill")
                fill_node.setNodeValue("#F3F3F3")
            svg = dom.toByteArray()

        renderer = QSvgRenderer(svg)
        renderer.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        renderer.render(painter, rect)


def draw_icon(
    icon: FIcon | QIcon,
    painter: QPainter,
    rect: QRect,
    state: QIcon.State = QIcon.State.Off,
) -> None:
    if isinstance(icon, FIcon):
        icon.render(painter, rect, state)
    else:
        icon.paint(painter, rect)
