from PySide6.QtCore import QEvent, QObject, QPointF, Qt
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from ...utils import set_font
from .title_bar_buttons import CloseButton, MaximizeButton, MinimizeButton


class TitleBarBase(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        # 需要此设置，否则background-color无效
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self._double_clicked_enabled = True

        # 固定高度，有两种模式：
        #   1.整体都高32，Label和Icon这些都是是顶格的
        #   2.整体高48，右侧三按钮仍然高32并居上，左侧的Label纵向居中
        #     适合显示地展示软件的Logo和名称，以及左上角做回退功能
        #     本UI暂时不考虑这种情况
        self.setFixedHeight(32)

        self.btn_minimize = MinimizeButton(self)
        self.btn_maximize = MaximizeButton(self)
        self.btn_close = CloseButton(self)

        self.btn_minimize.clicked.connect(self.window().showMinimized)
        self.btn_maximize.clicked.connect(self._toggle_maximize)
        self.btn_close.clicked.connect(self.window().close)

        self.window().installEventFilter(self)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if self._allow_move(event.position()):
            self.window().windowHandle().startSystemMove()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self._double_clicked_enabled:
            self._toggle_maximize()

    def setDoubleClickedEnabled(self, enabled: bool) -> None:
        self._double_clicked_enabled = enabled

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched is self.window() and event.type() == QEvent.Type.WindowStateChange:
            self.btn_maximize.set_max_state(self.window().isMaximized())

        return super().eventFilter(watched, event)

    def _allow_move(self, pos: QPointF) -> bool:
        # for btn in self.findChildren(TitleBarButton):
        #     if btn.isPressed():
        #         return False
        return True

    def _toggle_maximize(self) -> None:
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()


class TitleBar(TitleBarBase):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        # 本UI强制横向布局，其中有细分3个布局：
        #   1.信息区，展示软件Logo、名称、文件操作等，左侧
        #   2.常用功能区，软件常用的功能、文件路径显示等，居中
        #   3.按钮去，最小化、最大化、关闭三个按钮，右侧
        self.hlyt = QHBoxLayout(self)
        self.hlyt.setSpacing(0)
        self.hlyt.setContentsMargins(0, 0, 0, 0)

        # 信息区
        self.hlyt_info = QHBoxLayout()
        self.hlyt_info.setSpacing(0)
        self.hlyt_info.setContentsMargins(0, 0, 0, 0)
        self.hlyt_info.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.hlyt.addLayout(self.hlyt_info)

        # 功能区
        self.hlyt_func = QHBoxLayout()
        self.hlyt_func.setSpacing(0)
        self.hlyt_func.setContentsMargins(0, 0, 0, 0)
        self.hlyt_func.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hlyt.addLayout(self.hlyt_func)

        # 按钮区
        self.hlyt_btn = QHBoxLayout()
        self.hlyt_btn.setSpacing(0)
        self.hlyt_btn.setContentsMargins(0, 0, 0, 0)
        self.hlyt_btn.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.hlyt.addLayout(self.hlyt_btn)

        self.setStretches()

        # 设置软件Logo与名称
        self.icon = QLabel(self)
        self.icon.setFixedSize(24, 24)
        self.hlyt_info.addWidget(self.icon)
        self.window().windowIconChanged.connect(self.setIcon)

        self.title = QLabel(self)
        set_font(self.title)
        self.hlyt_info.addWidget(self.title)
        self.window().windowTitleChanged.connect(self.setTitle)

        # 三个按钮
        self.hlyt_btn.addWidget(self.btn_minimize)
        self.hlyt_btn.addWidget(self.btn_maximize)
        self.hlyt_btn.addWidget(self.btn_close)

    def setIcon(self, icon: QIcon) -> None:
        self.icon.setPixmap(icon.pixmap(self.icon.size()))

    def setTitle(self, title="") -> None:
        self.title.setText(title)

    def setStretches(self, stretches: tuple[int, int, int] = (1, 4, 1)) -> None:
        self.hlyt.setStretch(0, stretches[0])
        self.hlyt.setStretch(1, stretches[1])
        self.hlyt.setStretch(2, stretches[2])
