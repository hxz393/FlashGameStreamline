"""
此类提供了设置界面的初始化、语言更新、打开设置对话框等功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from lib.get_resource_path import get_resource_path
from ui.config_manager import ConfigManager
from ui.dialog_settings_main import DialogSettingsMain
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class ActionSettingMain(QObject):
    """
    设置界面操作类。

    :param lang_manager: 语言管理器，用于设置和更新界面语言。
    :param config_manager: 配置管理器，用于读取和修改设置。
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        self.init_ui()

    def init_ui(self) -> None:
        """
        初始化用户界面组件。

        :return: 无返回值。
        """
        self.action_setting = QAction(QIcon(get_resource_path('media/icons8-setting-26.png')), 'Settings')
        self.action_setting.setShortcut('F11')
        self.action_setting.triggered.connect(self.open_dialog)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_setting.setText(self.lang['ui.action_setting_1'])
        self.action_setting.setStatusTip(self.lang['ui.action_about_2'])

    def open_dialog(self) -> None:
        """
        打开设置对话框。

        :return: 无返回值。
        """
        try:
            self.dialog_settings_main = DialogSettingsMain(self.lang_manager, self.config_manager)
            self.dialog_settings_main.status_updated.connect(self.forward_status)
            self.dialog_settings_main.exec_()
        except Exception:
            logger.exception("An error occurred while opening the settings dialog")
            self.status_updated.emit(self.lang['label_status_error'])

    def forward_status(self, message: str) -> None:
        """
        用于转发状态信号。

        :param message: 要转发的消息。
        :return: 无返回值。
        """
        self.status_updated.emit(message)
