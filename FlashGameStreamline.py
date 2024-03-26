"""
Flash 网页游戏加速工具。通过运行代理，阻止指定资源下载来达到加速目的。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging
import os
import sys

from PyQt5.QtGui import QIcon, QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QToolBar

from config.settings import LOG_PATH, PROGRAM_NAME, CONFIG_MAIN_PATH, DEFAULT_CONFIG_MAIN, DEFAULT_CONFIG_USER
from lib.get_resource_path import get_resource_path
from lib.hide_console import hide_console
from lib.logging_config import logging_config
from lib.write_json import write_json
from ui import (Global_Signals, LangManager, ConfigManager, StatusBar, MainTable,
                ActionStart, ActionExit, ActionSettingMain, ActionLogs, ActionUpdate, ActionAbout,
                ActionEnable, ActionDisable, ActionAdd, ActionEdit, ActionDelete)

logger = logging.getLogger(__name__)


class FlashGameStreamLine(QMainWindow):
    """
    主窗口类。此类创建并管理应用程序的主界面，包括状态栏、表格和工具栏等组件。它还负责处理用户的操作和界面更新。
    """

    def __init__(self):
        super().__init__()
        # 初始化配置文件
        self.init_config()
        self.lang_manager = LangManager()
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = ConfigManager()
        self.init_ui()

    @staticmethod
    def init_config() -> None:
        """
        检查并初始化配置文件，配置文件若不存在，创建写入默认配置。

        :return: 无返回值。
        """
        try:
            if not os.path.isfile(CONFIG_MAIN_PATH):
                write_json(CONFIG_MAIN_PATH, DEFAULT_CONFIG_MAIN)
                write_json(DEFAULT_CONFIG_MAIN['config_user_path'], DEFAULT_CONFIG_USER)
        except Exception:
            logger.exception("Failed to initialize configuration")

    def init_ui(self) -> None:
        """
        初始化用户界面组件。

        :return: 无返回值。
        """
        # 创建状态栏
        self.status_bar = StatusBar(self.lang_manager)
        # 创建表单
        self.table = MainTable(self.lang_manager, self.config_manager)
        # 创建动作和连接信号
        self._create_action()
        # 创建菜单栏
        self._create_menubar()
        # 创建工具栏
        self._create_toolbar()
        # 主窗口配置
        self._configure_main_window()
        # 更新主界面文字
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.menu_run.setTitle(self.lang['main_2'])
        self.menu_edit.setTitle(self.lang['main_3'])
        self.menu_help.setTitle(self.lang['main_5'])

    def _create_action(self) -> None:
        """
        创建应用程序的动作，并连接信号和槽。

        :return: 无返回值。
        """
        self.table.status_updated.connect(self.status_bar.show_message)
        self.actionStart = ActionStart(self.lang_manager, self.config_manager)
        self.actionStart.status_updated.connect(self.status_bar.show_message)
        self.actionSettingMain = ActionSettingMain(self.lang_manager, self.config_manager)
        self.actionSettingMain.status_updated.connect(self.status_bar.show_message)
        self.actionExit = ActionExit(self.lang_manager)
        self.actionExit.status_updated.connect(self.status_bar.show_message)
        self.actionLogs = ActionLogs(self.lang_manager)
        self.actionLogs.status_updated.connect(self.status_bar.show_message)
        self.actionUpdate = ActionUpdate(self.lang_manager)
        self.actionUpdate.status_updated.connect(self.status_bar.show_message)
        self.actionAbout = ActionAbout(self.lang_manager)
        self.actionAbout.status_updated.connect(self.status_bar.show_message)
        self.actionEnable = ActionEnable(self.lang_manager, self.config_manager, self.table)
        self.actionEnable.status_updated.connect(self.status_bar.show_message)
        self.actionDisable = ActionDisable(self.lang_manager, self.config_manager, self.table)
        self.actionDisable.status_updated.connect(self.status_bar.show_message)
        self.actionAdd = ActionAdd(self.lang_manager, self.config_manager, self.table)
        self.actionAdd.status_updated.connect(self.status_bar.show_message)
        self.actionEdit = ActionEdit(self.lang_manager, self.config_manager, self.table)
        self.actionEdit.status_updated.connect(self.status_bar.show_message)
        self.actionDelete = ActionDelete(self.lang_manager, self.config_manager, self.table)
        self.actionDelete.status_updated.connect(self.status_bar.show_message)

    def _create_menubar(self) -> None:
        """
        创建菜单栏。

        :return: 无返回值。
        """
        menubar = self.menuBar()

        self.menu_run = menubar.addMenu("")
        self.menu_run.addAction(self.actionStart.action_start)
        self.menu_run.addAction(self.actionSettingMain.action_setting)
        self.menu_run.addSeparator()
        self.menu_run.addAction(self.actionExit.action_exit)
        self.menu_edit = menubar.addMenu("")
        self.menu_edit.addAction(self.actionEnable.action_enable)
        self.menu_edit.addAction(self.actionDisable.action_disable)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.actionAdd.action_add)
        self.menu_edit.addAction(self.actionEdit.action_edit)
        self.menu_edit.addAction(self.actionDelete.action_delete)
        self.menu_help = menubar.addMenu("")
        self.menu_help.addAction(self.actionLogs.action_logs)
        self.menu_help.addSeparator()
        self.menu_help.addAction(self.actionUpdate.action_update)
        self.menu_help.addAction(self.actionAbout.action_about)

    def _create_toolbar(self) -> None:
        """
        创建工具栏。

        :return: 无返回值。
        """
        self.toolbar = QToolBar('ToolBar', self)
        self.toolbar.setMovable(False)

        self.toolbar.addAction(self.actionStart.action_start)
        self.toolbar.addAction(self.actionSettingMain.action_setting)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionLogs.action_logs)
        self.toolbar.addAction(self.actionExit.action_exit)

    def _configure_main_window(self) -> None:
        """
        配置主窗口的基本属性。

        :return: 无返回值。
        """
        # 设置窗口大小、图标和名称
        self.setGeometry(10, 10, 400, 400)
        self.setWindowTitle(PROGRAM_NAME)
        self.setWindowIcon(QIcon(get_resource_path('media/main.ico')))
        # 创建垂直布局，加入表格
        self.addToolBar(self.toolbar)
        self.setStatusBar(self.status_bar)
        self.main_area = QVBoxLayout()
        self.main_area.addWidget(self.table)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_area)
        self.central_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

        # 移动窗口到屏幕中心
        self._center_window()
        # 展示主窗口
        self.show()

    def _center_window(self) -> None:
        """
        将窗口移动到屏幕中心。

        :return: 无返回值。
        :rtype: None
        """
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) / 2
        y = (screen.height() - self.height()) / 2
        self.move(int(x), int(y))

    def closeEvent(self, event: QCloseEvent):
        """
        重写关闭事件。当关闭主窗口时，此方法将被调用。它负责发送关闭信号并处理异常。

        :param event: 关闭事件对象。
        :return: 无返回值。
        """
        try:
            Global_Signals.close_all.emit()
        except Exception:
            logger.exception("Error encountered while sending close signal")
            event.ignore()
        else:
            event.accept()


def main() -> None:
    """
    应用程序的主入口函数，负责初始化和启动应用程序。

    :return: 无返回值。
    """
    try:
        app = QApplication(sys.argv)
        _ = FlashGameStreamLine()
        sys.exit(app.exec_())
    except Exception:
        logger.exception("Application failed to start")


if __name__ == '__main__':
    # 应用程序启动时调用，隐藏大黑框控制台，调整日志设置
    logging_config(log_file=LOG_PATH, console_output=True, max_log_size=1, log_level='INFO')
    hide_console()
    main()
