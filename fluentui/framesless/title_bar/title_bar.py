from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from .title_bar_buttons import (
    CloseButton,
    MaximizeButton,
    MinimizeButton,
    TitleBarButton,
)


class TitleBar(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.setMouseTracking(True)

        # 需要此设置，否则background-color无效
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        # 固定高度，有两种模式：
        #   1.整体都高32，Label和Icon这些都是是顶格的
        #   2.整体高48，右侧三按钮仍然高32并居上，左侧的Label纵向居中
        #     适合显示地展示软件的Logo和名称，以及左上角做回退功能
        #     本UI暂时不考虑这种情况
        self.setFixedHeight(32)

        # 本UI强制横向布局，其中有细分3个布局：
        #   1.信息区，展示软件Logo、名称、文件操作等，靠最左侧
        #   2.常用功能区，软件常用的功能、文件路径显示等，居中
        #   3.按钮去，最小化、最大化、关闭三个按钮，靠最右侧
        self.bar_layout = QHBoxLayout(self)
        self.bar_layout.setSpacing(50)
        self.bar_layout.setContentsMargins(0, 0, 0, 0)

        # 信息区
        self.info_layout = QHBoxLayout()
        self.info_layout.setSpacing(0)
        self.info_layout.setContentsMargins(0, 0, 0, 0)
        self.bar_layout.addLayout(self.info_layout, 1)

        # 功能区
        self.func_layout = QHBoxLayout()
        self.func_layout.setSpacing(20)
        self.func_layout.setContentsMargins(0, 0, 0, 0)
        self.bar_layout.addLayout(self.func_layout, 4)

        # 按钮区
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setSpacing(0)
        self.btn_layout.setContentsMargins(0, 0, 0, 0)
        self.bar_layout.addLayout(self.btn_layout, 1)

        # 设置软件Logo与名称
        self.icon = QLabel()
        self.icon.setFixedSize(22, 22)  # 原代码是18，我觉得太小了
        self.info_layout.addWidget(
            self.icon, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.window().windowIconChanged.connect(self.setIcon)
        self.title = QLabel()
        self.info_layout.addWidget(
            self.title, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.window().windowTitleChanged.connect(self.setTitle)
        self.info_layout.addStretch(0)  # stretch自动加在最右侧

        # 添加三按钮以及连接信号槽
        self.btn_minimize = MinimizeButton(self)
        self.btn_maximize = MaximizeButton(self)
        self.btn_close = CloseButton(self)
        # self.bar_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignVCenter)
        self.btn_layout.addStretch(0)  # 必须要addStretch，否则三个按钮就会被分开
        self.btn_layout.addWidget(
            self.btn_minimize,
            0,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
        )
        self.btn_layout.addWidget(
            self.btn_maximize,
            0,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
        )
        self.btn_layout.addWidget(
            self.btn_close, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop
        )
        self.btn_minimize.clicked.connect(self.window().showMinimized)
        self.btn_maximize.clicked.connect(self.on_btn_maximize_clicked)
        self.btn_close.clicked.connect(self.window().close)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # 原代码里分别在utils和window_effect中实现了，但usage只有前者
        # 猜测后者是早期写的，后来为了跨平台写了前者，但后者没删掉
        if self._allow_move(event.position()):
            self.window().windowHandle().startSystemMove()

        return super().mouseMoveEvent(event)

    def on_btn_maximize_clicked(self) -> None:
        is_max = self.window().isMaximized()
        if is_max:
            self.window().showNormal()
        else:
            self.window().showMaximized()
        self.btn_maximize.set_max_state(not is_max)

    def setIcon(self, icon: QIcon) -> None:
        self.icon.setPixmap(icon.pixmap(self.icon.size()))

    def setTitle(self, title="") -> None:
        self.title.setText(title)

    def _allow_move(self, pos: QPointF) -> bool:
        # cannot move if the mouse is pressed the widgets
        for btn in self.findChildren(TitleBarButton):
            if btn.is_pressed():
                return False
        return True
