from PySide6.QtGui import QAction

from .icon import Icon


class FAction(QAction):
    def __init__(self, icon: Icon = None, text: str = None, parent=None) -> None:
        super().__init__(parent=parent)

        self._icon = icon
        self._text = text

    def icon(self) -> Icon:
        return self._icon

    def setIcon(self, icon: Icon) -> None:
        self._icon = icon

    def text(self) -> str:
        return self._text

    def setText(self, text: str) -> None:
        self._text = text
