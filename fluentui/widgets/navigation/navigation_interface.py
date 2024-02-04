from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from ...utils import FIcon
from .navigation_panel import NavigationPanel, PanelPosition
from .navigation_widget import NavigationWidget


class NavigationInterface(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.panel = NavigationPanel(self)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(48, self.height())
        self.setMinimumWidth(48)

    def addWidget(
        self,
        widget: NavigationWidget,
        on_clicked: Callable = None,
        position: PanelPosition = PanelPosition.TOP,
    ) -> None:
        self.panel.addWidget(widget, on_clicked, position)

    def insertWidget(
        self,
        index: int,
        widget: NavigationWidget,
        on_clicked: Callable = None,
        position: PanelPosition = PanelPosition.TOP,
    ) -> None:
        self.panel.insertWidget(index, widget, on_clicked, position)

    def addItem(
        self,
        icon: FIcon,
        text: str,
        on_clicked: Callable = None,
        position: PanelPosition = PanelPosition.TOP,
    ) -> None:
        self.panel.addItem(icon, text, on_clicked, position)

    def insertItem(
        self,
        index: int,
        icon: FIcon,
        text: str,
        on_clicked: Callable = None,
        position: PanelPosition = PanelPosition.TOP,
    ) -> None:
        self.panel.insertItem(index, icon, text, on_clicked, position)

    def addSeperator(self, position: PanelPosition = PanelPosition.TOP) -> None:
        self.panel.addSeperator(position)

    def insertSeperator(
        self, index: int, position: PanelPosition = PanelPosition.TOP
    ) -> None:
        self.panel.insertSeperator(index, position)

    def toggle(self) -> None:
        self.panel.toggle()

    def expand(self) -> None:
        self.panel.expand()

    def collapse(self) -> None:
        self.panel.collapse()

    def setCurrentItem(self, name: str) -> None:
        self.panel.setCurrentItem(name)
