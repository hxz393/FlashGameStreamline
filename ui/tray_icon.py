"""
此模块提供程序托盘功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QAction

from lib.get_resource_path import get_resource_path
from ui.action_about import ActionAbout
from ui.action_exit import ActionExit
from ui.action_logs import ActionLogs
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class TrayIcon(QSystemTrayIcon):
    """
    托盘配置类。

    :param lang_manager: 语言管理器，用于处理语言更新。
    :param parent: 主窗口。
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 parent: QMainWindow = None):
        super(TrayIcon, self).__init__(parent)
        self.parent = parent
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        # 初始化在托盘右键菜单中显示的实例
        self.actionExit = ActionExit(self.lang_manager)
        self.actionExit.status_updated.connect(self.forward_status)
        self.actionLogs = ActionLogs(self.lang_manager)
        self.actionLogs.status_updated.connect(self.forward_status)
        self.actionAbout = ActionAbout(self.lang_manager)
        self.actionAbout.status_updated.connect(self.forward_status)
        self.init_ui()

    def init_ui(self) -> None:
        """
        初始化用户界面。

        :return: 无返回值。
        """
        # 创建系统托盘图标
        self.setIcon(QIcon(get_resource_path('media/main.ico')))

        # 还原动作
        self.action_restore = QAction(QIcon(get_resource_path('media/icons8-restore-window-26.png')), 'Restore')
        self.action_restore.triggered.connect(self.parent.showNormal)

        # 配置右键菜单
        tray_menu = QMenu()
        tray_menu.addAction(self.action_restore)
        tray_menu.addSeparator()
        tray_menu.addAction(self.actionLogs.action_logs)
        tray_menu.addAction(self.actionAbout.action_about)
        tray_menu.addSeparator()
        tray_menu.addAction(self.actionExit.action_exit)

        self.setContextMenu(tray_menu)
        self.activated.connect(self.tray_icon_clicked)

        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_restore.setText(self.lang['ui.action_restore_1'])
        self.action_restore.setStatusTip(self.lang['ui.action_restore_2'])

    def tray_icon_clicked(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """
        处理系统托盘图标被激活的事件。单击托盘图标时切换主窗口的显示状态。

        可用激活的原因（reason）：
          - QSystemTrayIcon.Trigger: 默认的激活原因，通常是单击。
          - QSystemTrayIcon.DoubleClick: 双击系统托盘图标。
          - QSystemTrayIcon.MiddleClick: 使用鼠标中键点击图标。

        :param reason: 触发此函数的激活动作。
        :return: 无返回值。
        """
        if reason == QSystemTrayIcon.Trigger:
            if self.parent.isVisible():
                self.parent.hide()
            else:
                self.parent.showNormal()
                self.parent.activateWindow()
                self.parent.raise_()

    def forward_status(self, message: str) -> None:
        """
        用于转发状态信号。

        :param message: 要转发的消息。
        :return: 无返回值。
        """
        self.status_updated.emit(message)
