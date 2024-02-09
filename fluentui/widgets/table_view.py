from PySide6.QtCore import QMargins, QModelIndex, QSize, Qt
from PySide6.QtGui import QColor, QPainter, QPalette
from PySide6.QtWidgets import (
    QAbstractItemView,
    QStyledItemDelegate,
    QStyleOptionViewItem,
)

from ..utils import ThemeColor


class TableItemDelegate(QStyledItemDelegate):
    def __init__(self, parent: QAbstractItemView):
        super().__init__(parent=parent)

        self._margin = 2
        self._hover_row = -1
        self._pressed_row = -1
        self._selected_rows = set()

    def set_hover_row(self, row: int) -> None:
        self._hover_row = row

    def set_pressed_row(self, row: int) -> None:
        self._pressed_row = row

    def set_selected_rows(self, indices: list[QModelIndex]) -> None:
        self._selected_rows.clear()
        for index in indices:
            self._selected_rows.add(index.row())
            if index.row() == self._pressed_row:
                self._pressed_row = -1

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        size = super().sizeHint(option, index)
        size = size.grownBy(QMargins(0, self._margin, 0, self._margin))

        return size

    # def createEditor(self, parent, option, index) -> None:

    # def updateEditorGeometry(self, editor, option, index) -> None:

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        super().initStyleOption(option, index)

        option.font = index.data(Qt.ItemDataRole.FontRole) or self.parent().font()

        text_color = QColor("black")
        text_brush = index.data(Qt.ItemDataRole.ForegroundRole)
        if text_brush is not None:
            text_color = text_brush.color()

        option.palette.setColor(QPalette.ColorRole.Text, text_color)
        option.palette.setColor(QPalette.ColorRole.HighlightedText, text_color)

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing
        )

        painter.setClipping(True)
        painter.setClipRect(option.rect)

        option.rect.adjusted(0, self._margin, 0, -self._margin)

        is_hover = self._hover_row == index.row()
        is_pressed = self._pressed_row == index.row()
        is_alternate = index.row() % 2 == 0 and self.parent().alternatingRowColors()

        alpha = 0
        if index.row() not in self._selected_rows:
            if is_pressed:
                alpha = 6
            elif is_hover:
                alpha = 12
            elif is_alternate:
                alpha = 5
        else:
            if is_pressed:
                alpha = 9
            elif is_hover:
                alpha = 25
            else:
                alpha = 17

        painter.setBrush(QColor(0, 0, 0, alpha))
        self._draw_background(painter, option, index)

        if (
            index.row() in self._selected_rows
            and index.column() == 0
            and self.parent().horizontalScrollBar().value() == 0
        ):
            self._draw_indicator(painter, option, index)

        if index.data(Qt.ItemDataRole.CheckStateRole) is not None:
            self._draw_check_box(painter, option, index)

        painter.restore()

        super().paint(painter, option, index)

    def _draw_background(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        r = 5
        if index.column() == 0:
            rect = option.rect.adjusted(4, 0, r + 1, 0)
            painter.drawRoundedRect(rect, r, r)
        elif index.column() == index.model().columnCount(index.parent()) - 1:
            rect = option.rect.adjusted(-r - 1, 0, -4, 0)
            painter.drawRoundedRect(rect, r, r)
        else:
            rect = option.rect.adjusted(-1, 0, 1, 0)
            painter.drawRect(rect)

    def _draw_indicator(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        y, h = option.rect.y(), option.rect.height()
        ph = round(0.35 * h if self._pressed_row == index.row() else 0.257 * h)
        painter.setBrush(ThemeColor.PRIMARY.color())
        painter.drawRoundedRect(4, ph + y, 3, h - 2 * ph, 1.5, 1.5)

    def _draw_check_box(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        pass
