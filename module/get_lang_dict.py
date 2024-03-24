"""
本模块提供了根据配置获取语言字典的功能。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging
from typing import Dict

from config.lang_dict_all import LANG_DICTS

from config.settings import CONFIG_MAIN_PATH, DEFAULT_CONFIG_MAIN
from lib.read_json_to_dict import read_json_to_dict

logger = logging.getLogger(__name__)


def get_lang_dict() -> Dict[str, str]:
    """
    本函数从配置文件中读取当前语言设置，并根据该设置返回对应的语言字典。如果读取配置时发生异常，将默认返回英文语言字典。

    :return: 语言字典，键为字符串标识，值为对应的翻译文本。
    """
    config_main = read_json_to_dict(CONFIG_MAIN_PATH) or DEFAULT_CONFIG_MAIN
    return LANG_DICTS[config_main.get('lang', 'English')]
