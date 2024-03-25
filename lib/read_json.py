"""
这个模块主要用于读取 JSON 文件。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393。保留所有权利。
"""
import json
import logging
import os
from typing import Dict, Union, Optional, List

logger = logging.getLogger(__name__)


def read_json(target_path: Union[str, os.PathLike]) -> Optional[Union[Dict, List]]:
    """
    读取 JSON 文件内容。

    :param target_path: Json 文件的路径，可以是字符串或 os.PathLike 对象。
    :return: 成功时返回内容字典或列表，如果遇到错误则返回 None。
    """
    try:
        with open(target_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        logger.exception(f"An error occurred while reading the JSON file '{target_path}'")
        return None
