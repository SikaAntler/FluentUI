from PySide6.QtCore import QEvent, QObject, QRectF, Qt
from PySide6.QtGui import (
    QFocusEvent,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPaintEvent,
)
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPlainTextEdit,
    QTextEdit,
    QToolButton,
    QWidget,
)

from ..utils import FIcon, FStyleSheet, ThemeColor, draw_icon, set_font


class FLineEditButton(QToolButton):
    ICON_SIZE = 12

    def __init__(self, icon: FIcon, parent=None) -> None:
        super().__init__(parent=parent)

        self._icon = icon

        self._is_pressed = False
        self.setFixedSize(31, 23)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._is_pressed = False
        super().mouseReleaseEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )

        rect = QRectF(
            (self.width() - self.ICON_SIZE) / 2,
            (self.height() - self.ICON_SIZE) / 2,
            self.ICON_SIZE,
            self.ICON_SIZE,
        )

        if self._is_pressed:
            painter.setOpacity(0.7)

        draw_icon(self._icon, painter, rect, fill="#656565")


class FLineEdit(QLineEdit):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setFixedHeight(33)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        FStyleSheet.LINE_EDIT.apply(self)
        set_font(self)

        self.hlyt = QHBoxLayout(self)
        self.hlyt.setSpacing(3)
        self.hlyt.setContentsMargins(4, 4, 4, 4)

        self._clear_button_enable = True
        self.btn_clear = FLineEditButton(FIcon.DISMISS, self)
        self.btn_clear.setFixedSize(29, 25)
        self.btn_clear.hide()
        self.hlyt.addWidget(
            self.btn_clear,
            0,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
        )

        self.btn_clear.clicked.connect(self.clear)
        self.textChanged.connect(self.on_text_changed)

    def isClearButtonEnabled(self) -> bool:
        return self._clear_button_enable

    def setClearButtonEnabled(self, enable: bool) -> None:
        self._clear_button_enable = enable
        self.setTextMargins(0, 0, 28 * enable, 0)

    def focusInEvent(self, event: QFocusEvent) -> None:
        super().focusInEvent(event)
        if self._clear_button_enable:
            self.btn_clear.setVisible(self.text() != "")

    def focusOutEvent(self, event: QFocusEvent) -> None:
        super().focusOutEvent(event)
        self.btn_clear.hide()

    def on_text_changed(self, text: str) -> None:
        if self._clear_button_enable:
            self.btn_clear.setVisible(text != "" and self.hasFocus())

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        if not self.hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        # 绘制底部横条
        m = self.contentsMargins()
        path = QPainterPath()
        w, h = self.width() - m.left() - m.right(), self.height()
        path.addRoundedRect(QRectF(m.left(), h - 10, w, 10), 5, 5)

        rect_path = QPainterPath()
        rect_path.addRect(m.left(), h - 10, w, 8)
        path = path.subtracted(rect_path)

        painter.fillPath(path, ThemeColor.PRIMARY.color())


class TextEditLayer(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        parent.installEventFilter(self)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched is self.parent() and event.type() == QEvent.Type.Resize:
            # self.resize(self.parent().size())
            self.resize(event.size())

        return super().eventFilter(watched, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        super().paintEvent(event)
        if not self.hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        m = self.contentsMargins()
        path = QPainterPath()
        w, h = self.width() - m.left() - m.right(), self.height()
        path.addRoundedRect(QRectF(m.left(), h - 10, w, 10), 5, 5)

        rect_path = QPainterPath()
        rect_path.addRect(m.left(), h - 10, w, 7.5)
        path = path.subtracted(rect_path)

        painter.fillPath(path, ThemeColor.PRIMARY.color())


class FPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.text_edit_layer = TextEditLayer(self)
        FStyleSheet.LINE_EDIT.apply(self)
        set_font(self)


class FTextEdit(QTextEdit):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.text_edit_layer = TextEditLayer(self)
        FStyleSheet.LINE_EDIT.apply(self)
        set_font(self)
