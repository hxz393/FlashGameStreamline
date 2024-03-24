"""
这个模块提供了配置初始化功能，主要用于检查和初始化各种配置文件。

模块的核心是 `init_config` 函数，它负责检查配置文件的存在性，若不存在则创建默认配置文件。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging
import os

from config.settings import DEFAULT_CONFIG_MAIN, CONFIG_MAIN_PATH
from lib.write_dict_to_json import write_dict_to_json

logger = logging.getLogger(__name__)


def init_config() -> None:
    """
    检查并初始化配置文件，配置文件若不存在，创建写入默认配置。

    :return: 无返回值。
    """
    try:
        if not os.path.isfile(CONFIG_MAIN_PATH):
            write_dict_to_json(CONFIG_MAIN_PATH, DEFAULT_CONFIG_MAIN)
    except Exception:
        logger.exception("Failed to initialize configuration")
