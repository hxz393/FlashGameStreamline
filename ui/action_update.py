"""
本模块提供软件更新检查功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from config.settings import VERSION_INFO, CHECK_UPDATE_URL
from lib.get_resource_path import get_resource_path
from lib.request_url import request_url
from ui.lang_manager import LangManager
from ui.message_show import message_show

logger = logging.getLogger(__name__)


class ActionUpdate(QObject):
    """
    软件更新检查操作的类。

    :param lang_manager: 语言管理器实例，用于更新界面语言。
    """
    status_updated = pyqtSignal(str)

    def __init__(self, lang_manager: LangManager):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.init_ui()

    def init_ui(self) -> None:
        """
        初始化更新操作的用户界面组件。

        :return: 无返回值。
        """
        self.action_update = QAction(QIcon(get_resource_path('media/icons8-update-26.png')), 'Update')
        self.action_update.setShortcut('F2')
        self.action_update.triggered.connect(self.check_update)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_update.setText(self.lang['ui.action_update_1'])
        self.action_update.setStatusTip(self.lang['ui.action_update_2'])

    def check_update(self) -> None:
        """
        检查软件是否有更新，检查结果以弹窗提示。

        :return: 无返回值。
        """
        self.action_update.setEnabled(False)
        self.status_updated.emit(self.lang['ui.action_update_8'])

        self.update_checker = UpdateChecker()
        self.update_checker.signal.connect(self.show_update_message)
        self.update_checker.start()

    def show_update_message(self, latest_version: str) -> None:
        """
        显示更新检查结果。

        :param latest_version: 最新版本号。
        :return: 无返回值。
        """
        self.action_update.setEnabled(True)
        self.status_updated.emit(self.lang['ui.action_update_9'])

        if latest_version is None:
            message_show('Warning', self.lang['ui.action_update_3'])
        elif latest_version == VERSION_INFO:
            message_show('Information', f"{self.lang['ui.action_update_5']}\n\n{self.lang['ui.action_update_7']}{VERSION_INFO}")
        else:
            message_show('Information', f"{self.lang['ui.action_update_4']}\n\n{self.lang['ui.action_update_6']}{VERSION_INFO}\n{self.lang['ui.action_update_7']}{latest_version}")


class UpdateChecker(QThread):
    """
    用于后台检查软件更新的线程类。

    """
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self) -> None:
        """
        执行更新检查的主要逻辑。此方法在线程启动时被调用，从指定的 URL 获取最新版本信息，并通过信号发送给主线程。

        :return: 无返回值。
        """
        try:
            latest_version = request_url(CHECK_UPDATE_URL)
            logger.info(f"The latest version: {latest_version}")
        except Exception:
            latest_version = None
            logger.exception("An error occurred while checking for updates")
        self.signal.emit(latest_version)
