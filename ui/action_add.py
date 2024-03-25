"""
本模块提供用户界面中的新增项功能。

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


class ActionAdd(QObject):
    """
    处理用户界面中新增操作的类。

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

        :param row: 要更新的行索引。
        :param url: url 地址。
        :param info: 包括描述和启用状态的映射字典。例如：{"active": true, "description": "xxx"}
        :return: 无返回值。
        """
        # 创建一个 QWidget 及其布局来存放复选框，并使其居中
        chk_box_widget = QWidget()
        chk_box_layout = QHBoxLayout(chk_box_widget)
        chk_box_layout.setAlignment(Qt.AlignCenter)
        chk_box_layout.setContentsMargins(0, 0, 0, 0)
        chk_box_item = QCheckBox()
        chk_box_item.setCheckState(Qt.Checked if info["active"] else Qt.Unchecked)
        chk_box_item.setEnabled(False)
        chk_box_layout.addWidget(chk_box_item)
        self.table.setCellWidget(row, 0, chk_box_widget)
        # 描述
        self.table.setItem(row, 1, QTableWidgetItem(info["description"]))
        # 地址
        self.table.setItem(row, 2, QTableWidgetItem(url))

    def add_item(self) -> None:
        """
        新增规则操作，并将其写入配置文件。

        :return: 无返回值。
        """
        try:
            # 获取配置
            config_user = self.config_manager.get_config('user')

            # 打开弹窗
            dialog = DialogTable(self.lang_manager)
            if dialog.exec_() == QDialog.Accepted:
                row_count = self.table.rowCount()
                info = {"active": False, "description": dialog.description_edit.text()}
                url = dialog.url_edit.text()
                self.table.insertRow(row_count)
                self.insert_row(row_count, url, info)
                # 插入新条目到配置
                config_user[url] = info

            # 更新配置管理器中的配置
            self.config_manager.update_config('user', config_user)
            # 发送到状态栏
            self.status_updated.emit(self.lang['ui.action_add_3'])
            logger.info("Item added.")
        except Exception:
            logger.exception("Error occurred while add item")
            self.status_updated.emit(self.lang['label_status_error'])
