from PySide6.QtCore import QEvent, QModelIndex, Qt
from PySide6.QtGui import QKeyEvent, QMouseEvent, QPainter, QResizeEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QListWidget,
    QListWidgetItem,
    QStyleOptionViewItem,
)

from ..utils import FStyleSheet, ThemeColor, set_font
from .scroll_bar import FSmoothScrollBar
from .table_view import TableItemDelegate


class ListItemDelegate(TableItemDelegate):
    def __init__(self, parent: QAbstractItemView):
        super().__init__(parent=parent)

    def _draw_background(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        painter.drawRoundedRect(option.rect, 5, 5)

    def _draw_indicator(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        y, h = option.rect.y(), option.rect.height()
        ph = round(0.35 * h if self._pressed_row == index.row() else 0.257 * h)
        painter.setBrush(ThemeColor.PRIMARY.color())
        painter.drawRoundedRect(0, ph + y, 3, h - 2 * ph, 1.5, 1.5)


class FListWidget(QListWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self._delegate = ListItemDelegate(self)
        self.setItemDelegate(self._delegate)

        self.scroll_bar_v = FSmoothScrollBar(Qt.Orientation.Vertical, self)
        self.scroll_bar_h = FSmoothScrollBar(Qt.Orientation.Horizontal, self)

        self._is_select_right_clicked_row = False

        self.setMouseTracking(True)

        self.entered.connect(lambda i: self._set_hover_row(i.row()))
        self.pressed.connect(lambda i: self._set_pressed_row(i.row()))

        FStyleSheet.LIST_VIEW.apply(self)
        set_font(self)

    def clearSelection(self) -> None:
        super().clearSelection()
        self._update_selected_rows()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)
        self._update_selected_rows()

    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)
        self._set_hover_row(-1)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if (
            event.button() == Qt.MouseButton.LeftButton
            or self._is_select_right_clicked_row
        ):
            super().mousePressEvent(event)
            return

        index = self.indexAt(event.pos())
        if index.isValid():
            self._set_pressed_row(index.row())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        super().mouseReleaseEvent(event)
        self._update_selected_rows()

        if (
            self.indexAt(event.pos()).row() < 0
            or event.button() == Qt.MouseButton.RightButton
        ):
            self._set_pressed_row(-1)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.viewport().update()

    def setCurrentIndex(self, index: QModelIndex) -> None:
        super().setCurrentIndex(index)
        self._update_selected_rows()

    def setCurrentItem(self, item: QListWidgetItem) -> None:
        self.setCurrentRow(self.row(item))

    def setCurrentRow(self, row: int) -> None:
        super().setCurrentRow(row)
        self._update_selected_rows()

    def _set_hover_row(self, row: int) -> None:
        self._delegate.set_hover_row(row)
        self.viewport().update()

    def _set_pressed_row(self, row: int) -> None:
        self._delegate.set_pressed_row(row)
        self.viewport().update()

    def _set_selected_row(self, indices: list[QModelIndex]) -> None:
        self._delegate.set_selected_rows(indices)
        self.viewport().update()

    def _update_selected_rows(self) -> None:
        self._set_selected_row(self.selectedIndexes())
