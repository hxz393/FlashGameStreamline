"""
本模块提供向列表中新增规则的功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QTableWidget, QDialog

from lib.get_resource_path import get_resource_path
from ui.config_manager import ConfigManager
from ui.dialog_table import DialogTable
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class ActionAdd(QObject):
    """
    新增规则操作的类。

    :param lang_manager: 语言管理器，用于处理界面语言设置。
    :param config_manager: 配置管理器，用于管理应用配置。
    :param table: 主表格对象。
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager,
                 table: QTableWidget):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        self.table = table
        self.init_ui()

    def init_ui(self) -> None:
        """
        初始化用户界面组件。

        :return: 无返回值。
        """
        self.action_add = QAction(QIcon(get_resource_path('media/icons8-add-26.png')), 'Add')
        self.action_add.setShortcut('F6')
        self.action_add.triggered.connect(self.add_item)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_add.setText(self.lang['ui.action_add_1'])
        self.action_add.setStatusTip(self.lang['ui.action_add_2'])

    def add_item(self) -> None:
        """
        往表格中新增规则条目，并更新配置文件。

        :return: 无返回值。
        """
        try:
            config_user = self.config_manager.get_config('user')
            dialog = DialogTable(self.lang_manager)

            # 打开输入弹窗输入内容，点击确定后更新配置
            if dialog.exec_() == QDialog.Accepted:
                config_user[dialog.url_edit.text()] = {"active": False, "description": dialog.description_edit.text()}

            self.config_manager.update_config('user', config_user)
            self.status_updated.emit(self.lang['ui.action_add_3'])
            logger.info("New Item added")
        except Exception:
            logger.exception("Error occurred while add item")
            self.status_updated.emit(self.lang['label_status_error'])
