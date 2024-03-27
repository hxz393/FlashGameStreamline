"""
提供应用程序的主要功能，启动代理和处理请求。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import asyncio
import logging
import socket
from threading import Thread
from typing import List

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from mitmproxy import http
from mitmproxy import options
from mitmproxy.http import HTTPFlow
from mitmproxy.tools.dump import DumpMaster

from config.settings import DEFAULT_CONFIG_USER, DEFAULT_CONFIG_MAIN
from lib.get_resource_path import get_resource_path
from ui.config_manager import ConfigManager
from ui.lang_manager import LangManager
from ui.message_show import message_show

logger = logging.getLogger(__name__)


class BlockAddon:
    """
    用于阻断指定 URL 请求的插件。

    :param patterns: 要阻止的 URL 列表。
    """

    def __init__(self, patterns: List[str]):
        self.patterns = patterns

    async def request(self, flow: HTTPFlow) -> None:
        """
        检查并处理每个请求的 URL 地址，如果请求的 URL 匹配到指定的模式之一，则阻断该请求。

        :param flow: 当前的 HTTP 请求流。
        :return: 无返回值。
        """
        # 遍历模式列表，检查每个模式是否在 URL 中
        for pattern in self.patterns:
            # 匹配到一个模式后，阻断连接，返回 403 状态码，不继续检查其他模式
            if pattern in flow.request.url:
                flow.response = http.Response.make(
                    403,
                    b"This URL is blocked.",
                    {"Content-Type": "text/plain"}
                )
                break


class LoggerAddon:
    """
    用于记录请求到日志的插件。
    """

    def __init__(self):
        pass

    @staticmethod
    async def response(flow: HTTPFlow) -> None:
        """
        记录每个 HTTP 响应的关键信息到日志。

        :param flow: 当前的 HTTP 请求流，包括请求和响应的信息。
        :return: 无返回值。
        """
        # 构建需要记录的信息字符串
        url = flow.request.url
        method = flow.request.method
        http_version = flow.request.http_version
        status_code = flow.response.status_code
        reason = flow.response.reason
        content_length_kb = len(flow.response.content) / 1024
        info = f"{method} {url} {http_version} << {status_code} {reason} {content_length_kb:.1f}KB"

        logging.warning(info) if status_code == 403 else logging.info(info)


class ActionStart(QObject):
    """
    启动代理动作类。

    :param lang_manager: 语言管理器，用于设置和更新界面语言。
    :param config_manager: 配置管理器，用于读取和修改设置。
    """
    status_updated = pyqtSignal(str)

    def __init__(self,
                 lang_manager: LangManager,
                 config_manager: ConfigManager):
        super().__init__()
        self.lang_manager = lang_manager
        self.lang_manager.lang_updated.connect(self.update_lang)
        self.config_manager = config_manager
        self.init_ui()

    def init_ui(self) -> None:
        """
        初始化用户界面。

        :return: 无返回值。
        """
        self.action_start = QAction(QIcon(get_resource_path('media/icons8-start-26.png')), 'Start')
        self.action_start.setShortcut('F10')
        self.action_start.triggered.connect(self.start)
        self.update_lang()

    def update_lang(self) -> None:
        """
        更新界面语言设置。

        :return: 无返回值。
        """
        self.lang = self.lang_manager.get_lang()
        self.action_start.setText(self.lang['ui.action_start_1'])
        self.action_start.setStatusTip(self.lang['ui.action_start_2'])

    def start(self) -> None:
        """
        启动服务的处理流程。

        :return: 无返回值。
        """
        try:
            config_user = self.config_manager.get_config('user') or DEFAULT_CONFIG_USER
            config_main = self.config_manager.get_config('main') or DEFAULT_CONFIG_MAIN
            port = int(config_main.get('server_port', 12345))
            patterns = [k for k, v in config_user.items() if v.get('active', False)]

            if not patterns:
                message_show('Warning', self.lang['ui.action_start_3'])
                return
            elif not self.is_port_available(port):
                message_show('Critical', self.lang['ui.action_start_5'])
                return
            else:
                # 开始按钮不可点击
                self.action_start.setEnabled(False)

            # 新开线程启动服务
            thread = Thread(target=self.start_proxy, args=(port, patterns))
            thread.daemon = True
            thread.start()

            self.status_updated.emit(self.lang['ui.action_start_4'])
        except Exception:
            logger.exception('Failed to start proxy!')
            self.status_updated.emit(self.lang['label_status_error'])

    @staticmethod
    def is_port_available(port: int) -> bool:
        """
        检查指定端口是否可用。

        :param port: 要检查的端口号。
        :return: 端口可用返回 True，否则返回 False。
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return True
            except OSError:
                return False

    def start_proxy(self,
                    port: int,
                    patterns: List[str]) -> None:
        """
        启动代理服务器。

        :param port: 监听端口。
        :param patterns: 拦截地址列表。
        :return: 无返回值。
        """
        asyncio.run(self.run_mitmproxy(port, patterns))

    @staticmethod
    async def run_mitmproxy(port: int, patterns: List[str]) -> None:
        """
        异步运行 mitmproxy 代理。

        :param port: 监听端口。
        :param patterns: 拦截地址列表。
        :return: 无返回值。
        """
        m = DumpMaster(options.Options(listen_port=port, http2=True))
        m.addons.add(BlockAddon(patterns))
        m.addons.add(LoggerAddon())

        try:
            await m.run()
        except Exception:
            print('错误〉！©')
            logger.exception("An error occurred!")
