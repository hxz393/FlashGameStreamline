"""
本模块提供向列表中新增规则的功能。

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

    def insert_row(self,
                   row: int,
                   url: str,
                   info: Dict[str, Union[str, bool]]) -> None:
        """
        向表格中插入一行数据。

        :param row: 要插入的行索引。
        :param url: 用于处理的 URL 地址。
        :param info: 包括描述和启用状态的映射字典。例如：{"active": true, "description": "xxx"}
        :return: 无返回值。
        """
        # 创建一个 QWidget 及其布局来存放启用状态复选框
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        check_box = QCheckBox()
        check_box.setCheckState(Qt.Checked if info["active"] else Qt.Unchecked)
        check_box.setEnabled(False)
        layout.addWidget(check_box)
        # 向单元格插入一行内容
        self.table.setCellWidget(row, 0, widget)
        self.table.setItem(row, 1, QTableWidgetItem(info["description"]))
        self.table.setItem(row, 2, QTableWidgetItem(url))

    def add_item(self) -> None:
        """
        往表格中新增规则条目，并更新配置文件。

        :return: 无返回值。
        """
        try:
            # 从配置管理器获取配置副本
            config_user = self.config_manager.get_config('user')
            dialog = DialogTable(self.lang_manager)
            # 打开输入弹窗输入内容，点击确定后将条目插入到表格末尾
            if dialog.exec_() == QDialog.Accepted:
                row = self.table.rowCount()
                info = {"active": False, "description": dialog.description_edit.text()}
                url = dialog.url_edit.text()
                self.table.insertRow(row)
                self.insert_row(row, url, info)
                # 更新配置
                config_user[url] = info

            # 更新配置管理器中的配置
            self.config_manager.update_config('user', config_user)
            # 发送到状态栏
            self.status_updated.emit(self.lang['ui.action_add_3'])
            logger.info("New Item added")
        except Exception:
            logger.exception("Error occurred while add item")
            self.status_updated.emit(self.lang['label_status_error'])
