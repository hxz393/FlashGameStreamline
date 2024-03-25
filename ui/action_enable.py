"""
本模块提供用户界面中的启用选中项功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QTableWidget

from lib.get_resource_path import get_resource_path
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class ActionEnable(QObject):
    """
    处理用户界面中启用操作的类。

    :param lang_manager: 语言管理器，用于处理界面语言设置。
    :param config_manager: 配置管理器，用于管理应用配置。
    :param table: 主表格界面对象。
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
        self.action_enable = QAction(QIcon(get_resource_path('media/icons8-toggle-on-26.png')), 'Enable')
        self.action_enable.setShortcut('F4')
        self.action_enable.triggered.connect(self.enable_items)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_enable.setText(self.lang['ui.action_enable_1'])
        self.action_enable.setStatusTip(self.lang['ui.action_enable_2'])

    def enable_items(self) -> None:
        """
        执行启用选中项目的操作，并将其写入配置文件。

        :return: 无返回值。
        """
        try:
            # 获取配置
            config_user = self.config_manager.get_config('user')
            rows = len(self.table.selectionModel().selectedRows())

            for item in self.table.selectedItems():
                row = item.row()
                # 设置复选框为勾选
                self.table.cellWidget(row, 0).layout().itemAt(0).widget().setChecked(True)
                # 更新配置中的启用状态
                config_user[self.table.item(row, 2).text()]['active'] = True

            # 更新配置管理器中的配置
            self.config_manager.update_config('user', config_user)
            # 发送到状态栏
            self.status_updated.emit(f"{rows} {self.lang['ui.action_enable_3']}")
            logger.info(f"{rows} Items enabled.")
        except Exception:
            logger.exception("Error occurred while enable items")
            self.status_updated.emit(self.lang['label_status_error'])
