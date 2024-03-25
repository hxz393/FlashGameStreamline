"""
这个模块主要用于将数据以 JSON 格式写入到文件。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""
import json
import logging
from pathlib import Path
from typing import Dict, Union, List

logger = logging.getLogger(__name__)


def write_json(target_path: Union[str, Path],
               data: Union[Dict, List]) -> bool:
    """
    将数据写入到 JSON 格式文件。

    :param target_path: Json 文件的路径，可以是字符串或 pathlib.Path 对象。
    :param data: 要写入的数据。
    :return: 成功时返回 True，失败时返回 False。
    """
    try:
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with target_path.open('w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except Exception:
        logger.exception(f"An error occurred while writing to the JSON file at '{target_path}'")
        return False
