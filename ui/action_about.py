"""
这个模块提供了一个打开关于对话框的动作类，用于显示关于信息。


:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from lib.get_resource_path import get_resource_path
from ui.dialog_about import DialogAbout
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class ActionAbout(QObject):
    """
    创建并管理打开关于对话框的动作。

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
        self.action_about = QAction(QIcon(get_resource_path('media/icons8-about-26.png')), 'About')
        self.action_about.setShortcut('F1')
        self.action_about.triggered.connect(self.open_dialog)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_about.setText(self.lang['ui.action_about_1'])
        self.action_about.setStatusTip(self.lang['ui.action_about_2'])

    def open_dialog(self) -> None:
        """
        打开关于对话框。

        :return: 无返回值。
        """
        try:
            dialog = DialogAbout(self.lang_manager)
            dialog.exec_()
        except Exception:
            logger.exception("An error occurred while opening the about dialog")
            self.status_updated.emit(self.lang['label_status_error'])
