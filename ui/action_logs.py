"""
此模块提供打开日志窗口功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from lib.get_resource_path import get_resource_path
from ui.dialog_logs import DialogLogs
from ui.global_signals import Global_Signals
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class ActionLogs(QObject):
    """
    此类负责创建日志查看的动作。

    :param lang_manager: 语言管理器，用于更新动作的显示语言。
    """
    status_updated = pyqtSignal(str)

    def __init__(self, lang_manager: LangManager):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.init_ui()

    def init_ui(self) -> None:
        """
        初始化用户界面组件。

        :return: 无返回值。
        """
        self.action_logs = QAction(QIcon(get_resource_path('media/icons8-log-26.png')), 'View Logs')
        self.action_logs.setShortcut('F3')
        self.action_logs.triggered.connect(self.open_dialog)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_logs.setText(self.lang['ui.action_logs_1'])
        self.action_logs.setStatusTip(self.lang['ui.action_logs_2'])

    def open_dialog(self) -> None:
        """
        打开日志对话框。

        :return: 无返回值。
        """
        try:
            # 实例化显示方式，非阻塞调用。阻塞调用为 self.dialog_logs.exec_()
            self.dialog_logs = DialogLogs(self.lang_manager)
            self.dialog_logs.status_updated.connect(self.forward_status)
            self.dialog_logs.show()
            # 连接全局信号，主窗口关闭时一并关闭日志窗口
            Global_Signals.close_all.connect(self.close_dialog)
        except Exception:
            logger.exception("An error occurred while opening the logs dialog")
            self.status_updated.emit(self.lang['label_status_error'])

    def close_dialog(self) -> None:
        """
        关闭日志对话框。由主窗口发送信号调用，避免主窗口关闭后，日志窗口还运行。

        :return: 无返回值。
        """
        if self.dialog_logs is not None:
            self.dialog_logs.close()

    def forward_status(self, message: str) -> None:
        """
        用于转发状态信号。

        :param message: 要转发的消息。
        :return: 无返回值。
        """
        self.status_updated.emit(message)
