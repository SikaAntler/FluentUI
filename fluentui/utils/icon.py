from enum import Enum

from PySide6.QtCore import QFile, QRect, QRectF, Qt
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtXml import QDomDocument


class Icon:
    def icon(self) -> QIcon:
        return QIcon(self.path())

    def path(self) -> str:
        raise NotImplementedError

    def render(
        self,
        painter: QPainter,
        rect: QRect | QRectF,
        state: QIcon.State,
        fill: str = None,
    ) -> None:
        svg_file = QFile(self.path())
        svg_file.open(QFile.OpenModeFlag.ReadOnly)
        svg = svg_file.readAll()
        svg_file.close()

        if state == QIcon.State.On or fill is not None:
            color = "#F3F3F3" if state == QIcon.State.On else fill

            dom = QDomDocument()
            dom.setContent(svg)
            node_list = dom.elementsByTagName("path")
            for i in range(node_list.length()):
                path_nodel = node_list.item(i)
                fill_node = path_nodel.attributes().namedItem("fill")
                fill_node.setNodeValue(color)
            svg = dom.toByteArray()

        renderer = QSvgRenderer(svg)
        renderer.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        renderer.render(painter, rect)


class FIcon(Icon, Enum):
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
    CARET_DOWN_FILLED = "caret_down_filled"
    CARET_LEFT_FILLED = "caret_left_filled"
    CARET_RIGHT_FILLED = "caret_right_filled"
    CARET_UP_FILLED = "caret_up_filled"
    CENTER_HORIZONTAL = "center_horizontal"
    CROP = "crop"
    DELETE = "delete"
    DISMISS = "dismiss"
    DRAW_TEXT = "draw_text"
    EDIT = "edit"
    ERROR_CIRCLE = "error_circle"
    FOLDER = "folder"
    FOLDER_OPEN = "folder_open"
    GROUP_LIST = "group_list"
    HOME = "home"
    IMAGE = "image"
    IMAGE_MULTIPLE = "image_multiple"
    IMAGE_SEARCH = "image_search"
    INFO = "info"
    LIGHTBULB = "lightbulb"
    LINE_HORIZONTAL_3 = "line_horizontal_3"
    MAXIMIZE = "maximize"
    OPEN_FOLDER = "open_folder"
    QUESTION_CIRCLE = "question_circle"
    RENAME = "rename"
    SAVE = "save"
    SCALE_FIT = "scale_fit"
    SCAN_CAMERA = "scan_camera"
    SEARCH = "search"
    SERIAL_PORT = "serial_port"
    SETTINGS = "settings"
    SQUARE = "square"
    TEXT = "text"
    WARNING = "warning"
    ZOOM_FIT = "zoom_fit"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"

    def path(self) -> str:
        return f":/fluentui/{self.value}"


def draw_icon(
    icon: Icon | QIcon,
    painter: QPainter,
    rect: QRect | QRectF,
    state: QIcon.State = QIcon.State.Off,
    fill: str = None,
) -> None:
    if isinstance(icon, Icon):
        icon.render(painter, rect, state, fill)
    else:
        rect = rect if isinstance(rect, QRect) else rect.toRect()
        icon.paint(painter, rect, state=state)
