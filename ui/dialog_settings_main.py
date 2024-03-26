"""
此模块提供了一个对话框界面，用于处理应用程序的主要设置。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLineEdit, QDialogButtonBox, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QComboBox, QPushButton, QFileDialog

from config.lang_dict_all import LANG_DICTS
from lib.get_resource_path import get_resource_path
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager

logger = logging.getLogger(__name__)


class DialogSettingsMain(QDialog):
    """
    主设置对话框类。

    :param lang_manager: 语言管理器实例。
    :param config_manager: 配置管理器实例。
    :ivar status_updated: 用于发出状态更新信号的 pyqtSignal 实例。
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager):
        super().__init__(flags=Qt.Dialog | Qt.WindowCloseButtonHint)
        # 初始化管理器
        self.lang_manager = lang_manager
        self.config_manager = config_manager
        # 获取管理器中的配置
        self.config_main = self.config_manager.get_config('main')
        # 获取语言字典
        self.lang = self.lang_manager.get_lang()
        self.init_ui()

    def init_ui(self) -> None:
        """
        初始化用户界面。

        :return: 无返回值。
        """
        # 主窗口
        self.setWindowTitle(self.lang['ui.dialog_settings_main_1'])
        self.setWindowIcon(QIcon(get_resource_path('media/icons8-setting-26')))
        self.setStyleSheet("font-size: 14px;")
        self.setMinimumSize(370, 230)

        # 主布局
        layout = QVBoxLayout()
        # 上层布局
        layout.addWidget(self._create_main_group())
        # 在两个组件之间添加弹性空间
        layout.addStretch()
        # 按钮布局
        layout.addLayout(self._create_buttons())

        self.setLayout(layout)

    def _create_main_group(self) -> QGroupBox:
        """
        创建并返回主要设置组的布局。

        :return: 配置好的主要设置组。
        """
        main_layout = QVBoxLayout()
        # 下拉框：选择语言
        self.language_combo_box = QComboBox()
        self.language_combo_box.addItems(LANG_DICTS.keys())
        self.language_combo_box.setCurrentText(self.config_main.get('lang', 'English'))
        main_layout.addWidget(QLabel(self.lang['ui.dialog_settings_main_2']))
        main_layout.addWidget(self.language_combo_box)
        # 输入框：服务端口
        self.port_line_edit = QLineEdit(self.config_main.get('server_port', ''))
        main_layout.addWidget(QLabel(self.lang['ui.dialog_settings_main_3']))
        main_layout.addWidget(self.port_line_edit)
        # 输入框：用户配置文件路径
        input_layout = QHBoxLayout()
        self.config_line_edit = QLineEdit(self.config_main.get('config_user_path', ''))
        input_layout.addWidget(self.config_line_edit)
        select_file_button = QPushButton(self.lang['ui.dialog_settings_main_6'], self)
        select_file_button.clicked.connect(self._open_file_dialog)
        input_layout.addWidget(select_file_button)
        main_layout.addWidget(QLabel(self.lang['ui.dialog_settings_main_4']))
        main_layout.addLayout(input_layout)
        # 分组
        main_group = QGroupBox(self.lang['ui.dialog_settings_main_5'])
        main_group.setStyleSheet("QGroupBox { font-weight: bold; text-align: center; }")
        main_group.setLayout(main_layout)
        return main_group

    def _create_buttons(self) -> QHBoxLayout:
        """
        创建并返回对话框底部的按钮布局。

        :return: 包含确定和取消按钮的布局。
        """
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText(self.lang['ui.dialog_settings_main_11'])
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText(self.lang['ui.dialog_settings_main_12'])
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(button_box)
        button_layout.setContentsMargins(0, 10, 0, 0)
        return button_layout

    def reject(self) -> None:
        """
        当用户点击取消按钮时，关闭对话框并忽略所有未保存的更改。

        :return: 无返回值。
        """
        super().reject()

    def accept(self) -> None:
        """
        当用户点击确认按钮时，此方法会更新配置，并尝试将其写入配置文件。如果成功，则发出状态更新信号；如果失败，则显示错误消息。

        :return: 无返回值。
        """
        try:
            # 对比语言值，有修改则在 LangManager 类中修改
            self._check_language_change()
            # 更新配置
            self._update_config()
            super().accept()
            logger.info("Settings saved")
        except Exception:
            logger.exception("Error while updating settings")
            self.status_updated.emit(self.lang['label_status_error'])

    def _open_file_dialog(self) -> None:
        """
        打开文件选择对话框，将文件路径填入对应文本框

        :return: 无返回值。
        """
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, self.lang['ui.dialog_settings_main_6'], "", "All Files (*);;Text Files (*.json)", options=options)
        if fileName:
            self.config_line_edit.setText(fileName)

    def _update_config(self) -> None:
        """
        从对话框中收集用户输入的数据，并更新配置。

        :return: 无返回值。
        """
        self.config_main['lang'] = self.language_combo_box.currentText()
        self.config_main['server_port'] = self.port_line_edit.text()
        self.config_main['config_user_path'] = self.config_line_edit.text()

        # 更新 ConfigManager 类实例中的配置
        self.config_manager.update_config('main', self.config_main)
        # 发送更新成功状态信号
        self.status_updated.emit(self.lang['ui.dialog_settings_main_13'])

    def _check_language_change(self) -> None:
        """
        检查语言设置是否更改。

        如果用户更改语言设置，要调用LangManager类的方法update_lang，发送新语言字符串。
        更新LangManager类实例中的self.lang_dict内容，并发送lang_updated信号。
        所有连接了LangManager类实例lang_updated信号的类，将会执行绑定的函数。
        一般是self.update_lang()，里面最先运行的就是更新自己的self.lang：
        self.lang = self.lang_manager.get_lang()
        然后是用方法更新各地方的显示字符串：
        self.action_about.setText(self.lang['ui.action_about_1'])

        :return: 无返回值。
        """
        if self.language_combo_box.currentText() != self.config_main.get('lang', 'English'):
            self.lang_manager.update_lang(self.language_combo_box.currentText())
