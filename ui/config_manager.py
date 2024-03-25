"""
这个模块提供了配置管理功能，主要用于处理和更新应用程序的配置信息。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import copy
import logging
from typing import Dict, Optional, Tuple, Any

from PyQt5.QtCore import QObject, pyqtSignal

from config.settings import CONFIG_MAIN_PATH, DEFAULT_CONFIG_MAIN, DEFAULT_CONFIG_USER
from lib.read_json import read_json
from lib.write_json import write_json

logger = logging.getLogger(__name__)


class ConfigManager(QObject):
    """
    配置管理器类，负责管理和更新应用程序的配置信息。

    该类包括获取和更新配置的方法，同时提供信号以通知配置更新。

    :ivar config_main_updated: 当主配置更新时发出的信号。
    :ivar config_user_updated: 当用户配置更新时发出的信号。
    """
    config_main_updated = pyqtSignal()
    config_user_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._config_main = read_json(CONFIG_MAIN_PATH) or DEFAULT_CONFIG_MAIN
        self._config_user = read_json(self._config_main.get('config_user_path', '')) or DEFAULT_CONFIG_USER

    def _get_config_objects(self, config_type: str) -> Tuple[Dict[str, Any], pyqtSignal, str]:
        """
        根据配置类型返回配置字典、更新信号和配置文件路径。

        :param config_type: 配置类型。
        :return: 配置字典、对应的更新信号和配置文件路径。
        """
        if config_type == 'main':
            return self._config_main, self.config_main_updated, CONFIG_MAIN_PATH
        else:
            return self._config_user, self.config_user_updated, self._config_main.get('config_user_path', DEFAULT_CONFIG_MAIN['config_user_path'])

    def get_config(self, config_type: str) -> Optional[Dict[str, Any]]:
        """
        获取配置的副本。

        :param config_type: 配置类型，可以是 'main' 或 'user'。
        :return: 包含配置的字典副本，如果出现错误则返回 None。
        """
        try:
            config, _, _ = self._get_config_objects(config_type)
            return copy.deepcopy(config)
        except Exception:
            logger.exception(f"Failed to get config: {config_type}")
            return None

    def update_config(self,
                      config_type: str,
                      new_config: Dict[str, Any]) -> None:
        """
        更新配置。

        :param config_type: 配置类型，可以是 'main' 或 'user'。
        :param new_config: 新的配置。
        :return: 无
        """
        try:
            config, signal, path = self._get_config_objects(config_type)
            signal.emit()
            write_json(path, new_config)
            logger.info(f"Config updated: {config_type}")
        except Exception:
            logger.exception(f"Failed to update config: {config_type}")
