"""
这个模块主要用于将列表以文本格式写入到文件。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""
import logging
from pathlib import Path
from typing import List, Any, Optional, Union, Set

logger = logging.getLogger(__name__)


def write_list_to_file(target_path: Union[str, Path],
                       content: Union[List[Any], Set[Any]]) -> Optional[bool]:
    """
    将列表的元素写入文件，每个元素占据文件的一行。

    :param target_path: 文本文件的路径，可以是字符串或 pathlib.Path 对象。
    :param content: 要写入的列表或元祖。
    :return: 成功时返回 True，失败时返回 False。
    """
    try:
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with target_path.open('w', encoding="utf-8") as file:
            file.write("\n".join(str(element) for element in content))
        return True
    except Exception:
        logger.exception(f"An error occurred while writing to the file at '{target_path}'")
        return False
