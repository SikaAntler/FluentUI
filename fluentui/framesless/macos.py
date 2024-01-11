import Cocoa
import objc
from PySide6.QtCore import Qt
from PySide6.QtGui import QPaintEvent, QResizeEvent

from .title_bar import TitleBar


# from PySide6.QtWidgets import QMainWindow
# class FramelessHelper(QMainWindow):
class FramelessHelper:
    def __init__(self) -> None:
        super().__init__()

        view = objc.objc_object(c_void_p=self.winId())
        self._ns_window = view.window()

        self.setMouseTracking(True)

        self.title_bar = TitleBar(self)

        self._hide_system_title_bar()

        # self.setContentsMargins(0, 32, 0, 0)

    def paintEvent(self, event: QPaintEvent) -> None:
        self._hide_system_title_bar()
        super().paintEvent(event)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.title_bar.resize(self.width(), self.title_bar.height())

    # def changeEvent(self, event: QEvent) -> None:
    #     if event.type() == QEvent.WindowStateChange:
    #         self._hide_system_title_bar()

    def _hide_system_title_bar(self) -> None:
        self._ns_window.setStyleMask_(
            self._ns_window.styleMask() | Cocoa.NSFullSizeContentViewWindowMask
        )
        self._ns_window.setTitlebarAppearsTransparent_(True)

        self._ns_window.setMovableByWindowBackground_(False)
        self._ns_window.setMovable_(False)

        self._ns_window.setShowsToolbarButton_(False)
        self._ns_window.setTitleVisibility_(Cocoa.NSWindowTitleHidden)
        self._ns_window.standardWindowButton_(Cocoa.NSWindowCloseButton).setHidden_(
            True
        )
        self._ns_window.standardWindowButton_(Cocoa.NSWindowZoomButton).setHidden_(True)
        self._ns_window.standardWindowButton_(
            Cocoa.NSWindowMiniaturizeButton
        ).setHidden_(True)

    def _set_window_flags(self, window_type: Qt.WindowType) -> None:
        self.setWindowFlags(
            window_type
            | Qt.WindowType.FramelessWindowHint
            # | Qt.WindowType.WindowSystemMenuHint
            | Qt.WindowType.WindowMinimizeButtonHint
        )
