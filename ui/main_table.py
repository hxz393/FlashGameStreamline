"""
此文件定义了 MainTable 类，一个基于 PyQt5 的 QTableWidget 的高级实现。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2023, hxz393. 保留所有权利。
"""

import logging
from typing import Dict, Union

from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtWidgets import QHeaderView, QMenu, QAction, QWidget, QHBoxLayout, QCheckBox, QTableWidgetItem
from PyQt5.QtWidgets import QTableWidget

from config.settings import DEFAULT_CONFIG_USER
from ui.action_add import ActionAdd
from ui.action_delete import ActionDelete
from ui.action_disable import ActionDisable
from ui.action_edit import ActionEdit
from ui.action_enable import ActionEnable
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class MainTable(QTableWidget):
    """
    主表格类，用于展示和管理数据行。

    :param lang_manager: 用于管理界面语言的 LangManager 实例。
    :param config_manager: 用于管理配置的 ConfigManager 实例。
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager):
        super().__init__()
        # 接受更新信号，更新语言和数据
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        self.config_manager.config_user_updated.connect(self.insert_data)
        # 实例化用到的编辑动作
        self.actionEnable = ActionEnable(self.lang_manager, self.config_manager, self)
        self.actionEnable.status_updated.connect(self.forward_status)
        self.actionDisable = ActionDisable(self.lang_manager, self.config_manager, self)
        self.actionDisable.status_updated.connect(self.forward_status)
        self.actionAdd = ActionAdd(self.lang_manager, self.config_manager, self)
        self.actionAdd.status_updated.connect(self.forward_status)
        self.actionEdit = ActionEdit(self.lang_manager, self.config_manager, self)
        self.actionEdit.status_updated.connect(self.forward_status)
        self.actionDelete = ActionDelete(self.lang_manager, self.config_manager, self)
        self.actionDelete.status_updated.connect(self.forward_status)
        # 先运行语言更新，里面有表头定义
        self.update_lang()
        self.init_ui()
        self.insert_data()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.column_headers = [
            self.lang['ui.table_main_1'],
            self.lang['ui.table_main_2'],
            self.lang['ui.table_main_3'],
        ]
        # 重新应用到表头
        self.setHorizontalHeaderLabels(self.column_headers)

    def init_ui(self) -> None:
        """
        初始化用户界面。

        :return: 无返回值。
        """
        # 配置表格基本属性
        self.setColumnCount(len(self.column_headers))
        self.setHorizontalHeaderLabels(self.column_headers)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setStyleSheet("QTableWidget {border: 0;}")
        self.setSelectionBehavior(QTableWidget.SelectRows)
        # 设置表头
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setMinimumSectionSize(50)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # 为表单设置右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._cell_context_menu)

    def insert_data(self) -> None:
        """
        向表格中插入全量数据。

        :return: 无返回值。
        """
        # 获取用户配置
        config_user = self.config_manager.get_config('user') or DEFAULT_CONFIG_USER
        # 设置行数，插入数据
        self.setRowCount(len(config_user))
        for row, (url, info) in enumerate(config_user.items()):
            self.insert_row(row, url, info)

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
        self.setCellWidget(row, 0, widget)
        self.setItem(row, 1, QTableWidgetItem(info["description"]))
        self.setItem(row, 2, QTableWidgetItem(url))

    def _cell_context_menu(self, pos: QPoint) -> None:
        """
        实现表格单元格的右键菜单功能。

        :param pos: 右键点击的位置。
        :return: 无返回值。
        """
        menu = QMenu(self)
        menu.addAction(self.actionEnable.action_enable)
        menu.addAction(self.actionDisable.action_disable)
        separator = QAction(menu)
        separator.setSeparator(True)
        menu.addAction(separator)
        menu.addAction(self.actionAdd.action_add)
        menu.addAction(self.actionEdit.action_edit)
        menu.addAction(self.actionDelete.action_delete)
        menu.exec_(self.viewport().mapToGlobal(pos))

    def forward_status(self, message: str) -> None:
        """
        用于转发状态信号。

        :param message: 要转发的消息。
        :return: 无返回值。
        """
        self.status_updated.emit(message)

    def get_data(self) -> Dict[str, Dict[str, any]]:
        """
        获取表格中的数据，未用到。

        :return: 返回数据字典，其中每个元素都是一个字典，包含了单元格的选中状态、描述和链接。
        """
        return {self.item(row, 2).text(): {"active": self.cellWidget(row, 0).layout().itemAt(0).widget().isChecked(), "description": self.item(row, 1).text()} for row in range(self.rowCount())}

    def clear(self) -> None:
        """
        清空表格中的所有行，未用到。

        :return: 无返回值。
        """
        try:
            # 禁用更新以提高性能
            self.setUpdatesEnabled(False)
            # 首先清除所有单元格的内容
            self.clearContents()
            # 将行数设置为0，从而删除所有行
            self.setRowCount(0)
        except Exception:
            logger.exception("Error occurred while clearing the table.")
            self.status_updated.emit(self.lang['label_status_error'])
        finally:
            # 确保即使发生错误也要重新启用更新
            self.setUpdatesEnabled(True)
