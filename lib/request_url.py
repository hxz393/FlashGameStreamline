"""
此模块主要用于发送HTTP GET请求并处理可能的异常。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging
from typing import Optional

import requests

requests.packages.urllib3.disable_warnings()
logger = logging.getLogger(__name__)


def request_url(url: str) -> Optional[str]:
    """
    通过 HTTP GET 请求获取给定 URL 的响应内容。

    :param url: 待请求的 URL
    :return: 如果请求成功，返回 URL 的响应内容；否则返回 None
    """
    session = requests.Session()
    session.trust_env = False

    try:
        response = session.get(url, verify=False, timeout=15)
        response.raise_for_status()
        return response.text.strip()
    except Exception:
        logger.exception(f"Unable to send network request to {url}")
        return None
