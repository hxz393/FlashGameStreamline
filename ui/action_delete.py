"""
本模块提供删除表格内选中项的功能。

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


class ActionDelete(QObject):
    """
    处理删除操作的类。

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
        self.action_delete = QAction(QIcon(get_resource_path('media/icons8-delete-26.png')), 'Delete')
        self.action_delete.setShortcut('F8')
        self.action_delete.triggered.connect(self.delete_items)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_delete.setText(self.lang['ui.action_delete_1'])
        self.action_delete.setStatusTip(self.lang['ui.action_delete_2'])

    def delete_items(self) -> None:
        """
        执行删除选中项目的操作，并更新配置文件。

        :return: 无返回值。
        """
        try:
            config_user = self.config_manager.get_config('user')
            # 获取选中行的索引，并按照从大到小的顺序排序，从而保证删除的顺序不会乱
            rows_to_delete = sorted([index.row() for index in self.table.selectionModel().selectedRows()], reverse=True)
            # 遍历并删除行，以及更新配置
            for row in rows_to_delete:
                config_user.pop(self.table.item(row, 2).text(), None)
                self.table.removeRow(row)

            self.config_manager.update_config('user', config_user)
            self.status_updated.emit(f"{len(rows_to_delete)} {self.lang['ui.action_delete_3']}")
            logger.info(f"{len(rows_to_delete)} Items deleted.")
        except Exception:
            logger.exception("Error occurred while delete items")
            self.status_updated.emit(self.lang['label_status_error'])
