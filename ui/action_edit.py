"""
本模块提供用户界面中的编辑项功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Union

from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QTableWidget, QDialog, QWidget, QHBoxLayout, QCheckBox, QTableWidgetItem

from lib.get_resource_path import get_resource_path
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager
from ui.dialog_table import DialogTable

logger = logging.getLogger(__name__)


class ActionEdit(QObject):
    """
    处理用户界面中编辑操作的类。

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
        self.action_edit = QAction(QIcon(get_resource_path('media/icons8-edit-26.png')), 'Edit')
        self.action_edit.setShortcut('F7')
        self.action_edit.triggered.connect(self.edit_item)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_edit.setText(self.lang['ui.action_edit_1'])
        self.action_edit.setStatusTip(self.lang['ui.action_edit_2'])

    def edit_item(self) -> None:
        """
        修改规则操作，并将其写入配置文件。

        :return: 无返回值。
        """
        try:
            # 获取配置
            config_user = self.config_manager.get_config('user')
            row = self.table.currentRow()
            # 打开弹窗
            dialog = DialogTable(self.lang_manager)
            # 插入数据到对话框
            dialog.description_edit.setText(self.table.item(row, 1).text())
            dialog.url_edit.setText(self.table.item(row, 2).text())
            if dialog.exec_() == QDialog.Accepted:
                # 根据行索引获取对应的配置键值
                key_to_delete = self.table.item(row, 2).text()
                if key_to_delete in config_user:
                    # 从配置中删除对应的键值对
                    del config_user[key_to_delete]
                self.table.item(row, 1).setText(dialog.description_edit.text())
                self.table.item(row, 2).setText(dialog.url_edit.text())
                # 修改配置中的条目
                config_user[dialog.url_edit.text()] = {"active": False, "description": dialog.description_edit.text()}

            # 更新配置管理器中的配置
            self.config_manager.update_config('user', config_user)
            # 发送到状态栏
            self.status_updated.emit(self.lang['ui.action_edit_3'])
            logger.info("Item modified.")
        except Exception:
            logger.exception("Error occurred while modify item")
            self.status_updated.emit(self.lang['label_status_error'])
