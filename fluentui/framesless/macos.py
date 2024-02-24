import Cocoa
import objc
from PySide6.QtCore import QEvent
from PySide6.QtGui import QPaintEvent, QResizeEvent
from PySide6.QtWidgets import QDialog, QMainWindow, QWidget

from .title_bar import TitleBar


class FramelessHelper:
    def __init__(self, parent=None) -> None:
        super().__init__()

        view = objc.objc_object(c_void_p=self.winId())
        self._ns_window = view.window()
        self._hide_system_title_bar()

        self.title_bar = TitleBar(self)

        self._enable_resize = True

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.Type.WindowStateChange:
            self._hide_system_title_bar()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.title_bar.resize(self.width(), self.title_bar.height())

    # def showEvent(self, event: QShowEvent) -> None:
    #     super().showEvent(event)
    #     self._hide_system_title_bar()
    #
    # def closeEvent(self, event: QCloseEvent) -> None:
    #     super().closeEvent(event)
    #     self._hide_system_title_bar()

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

    # def _set_window_flags(self, window_type: Qt.WindowType) -> None:
    #     self.setWindowFlags(window_type)


class MacOSFramelessDialog(FramelessHelper, QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.title_bar.btn_minimize.hide()
        self.title_bar.btn_maximize.hide()
        self.title_bar.setDoubleClickedEnabled(False)

    def changeEvent(self, event: QEvent) -> None:
        FramelessHelper.changeEvent(self, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        QDialog.paintEvent(self, event)
        self._hide_system_title_bar()

    def resizeEvent(self, event: QResizeEvent) -> None:
        FramelessHelper.resizeEvent(self, event)


class MacOSFramelessMainWindow(FramelessHelper, QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setMenuWidget(self.title_bar)

    def changeEvent(self, event: QEvent) -> None:
        # QMainWindow.changeEvent(self, event)
        FramelessHelper.changeEvent(self, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        QMainWindow.paintEvent(self, event)
        self._hide_system_title_bar()

    def resizeEvent(self, event: QResizeEvent) -> None:
        # QMainWindow.resizeEvent(self, event)
        FramelessHelper.resizeEvent(self, event)


class MacOSFramelessWidget(FramelessHelper, QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

    def changeEvent(self, event: QEvent) -> None:
        FramelessHelper.changeEvent(self, event)

    def paintEvent(self, event: QPaintEvent) -> None:
        QWidget.paintEvent(self, event)
        self._hide_system_title_bar()

    def resizeEvent(self, event: QResizeEvent) -> None:
        FramelessHelper.resizeEvent(self, event)
