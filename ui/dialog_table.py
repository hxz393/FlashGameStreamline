"""
本模块提供定义了一个表格用的对话框，用于新增和修改数据。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

from lib.get_resource_path import get_resource_path
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class DialogTable(QDialog):
    """
    弹出交互对话框，用于表格内容修改新增。

    :param lang_manager: 语言管理器，用于更新动作的显示语言。
    """

    def __init__(self, lang_manager: LangManager):
        super().__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        self.lang_manager = lang_manager
        self.lang = self.lang_manager.get_lang()
        self.init_ui()

    def init_ui(self) -> None:
        """
        初始化用户界面组件。

        :return: 无返回值。
        """
        self.setWindowTitle(self.lang['ui.dialog_table_1'])
        self.setWindowIcon(QIcon(get_resource_path('media/icons8-log-26.png')))
        # 添加元素
        layout = QVBoxLayout(self)
        # 描述信息
        self.description_edit = QLineEdit(self)
        layout.addWidget(QLabel(f"{self.lang['ui.table_main_2']}:"))
        layout.addWidget(self.description_edit)
        # 地址信息
        self.url_edit = QLineEdit(self)
        layout.addWidget(QLabel(f"{self.lang['ui.table_main_3']}:"))
        layout.addWidget(self.url_edit)
        # 在两个组件之间添加弹性空间
        layout.addStretch()
        # 确认按钮
        self.ok_button = QPushButton(self.lang['ui.dialog_settings_main_11'], self)
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
