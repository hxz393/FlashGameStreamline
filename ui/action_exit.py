"""
本模块提供程序退出功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QCoreApplication, pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from lib.get_resource_path import get_resource_path
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class ActionExit(QObject):
    """
    退出动作的类。

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
        self.action_exit = QAction(QIcon(get_resource_path('media/icons8-exit-26.png')), 'Exit')
        self.action_exit.setShortcut('Ctrl+Q')
        self.action_exit.triggered.connect(self.exit)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_exit.setText(self.lang['ui.action_exit_1'])
        self.action_exit.setStatusTip(self.lang['ui.action_exit_2'])

    def exit(self) -> None:
        """
        执行退出操作。

        :return: 无返回值。
        """
        try:
            QCoreApplication.quit()
        except Exception:
            logger.exception("Exiting application error")
            self.status_updated.emit(self.lang['label_status_error'])
