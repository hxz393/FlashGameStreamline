"""
此模块包含语言管理相关功能，用于处理多语言环境下的语言字典的获取和更新。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import copy
import logging
from typing import Dict, Optional

from PyQt5.QtCore import QObject, pyqtSignal

from config.lang_dict_all import LANG_DICTS
from config.settings import DEFAULT_CONFIG_MAIN, CONFIG_MAIN_PATH
from lib.read_json import read_json

logger = logging.getLogger(__name__)


class LangManager(QObject):
    """
    语言管理类，用于管理和更新应用程序的语言字典。

    :ivar _lang_dict: 当前使用的语言字典。
    """
    lang_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        config_main = read_json(CONFIG_MAIN_PATH) or DEFAULT_CONFIG_MAIN
        self._lang_dict = LANG_DICTS[config_main.get('lang', 'English')]

    def get_lang(self) -> Optional[Dict[str, str]]:
        """
        获取当前使用的语言字典的副本。

        :return: 当前语言字典的深拷贝。
        """
        try:
            return copy.deepcopy(self._lang_dict)
        except Exception:
            logger.exception("Failed to retrieve language dictionary.")
            return None

    def update_lang(self, new_lang: str) -> None:
        """
        更新当前使用的语言字典。

        :param new_lang: 新语言的标识符。
        :return: 无返回值。
        """
        try:
            self._lang_dict = LANG_DICTS.get(new_lang, "English")
            self.lang_updated.emit()
            logger.info(f"Language changed to {new_lang}")
        except Exception:
            logger.exception(f"Failed to changed language to {new_lang}")
