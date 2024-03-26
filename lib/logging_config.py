"""
`logging_config`函数的目标是配置日志记录器。可以选择在控制台输出，也可以选择记录到日志文件。返回配置后的日志记录器实例。

函数使用了日志记录器记录任何在转换过程中发生的错误。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""
import logging
import os
from logging import getLogger, StreamHandler, Formatter
from logging.handlers import RotatingFileHandler
from typing import Optional


def logging_config(log_file: Optional[str] = None,
                   console_output: bool = False,
                   log_level: str = 'NOTSET',
                   max_log_size: int = 10,
                   backup_count: int = 10,
                   default_log_format: str = '%(asctime)s - %(levelname)s - %(module)s::%(funcName)s::%(lineno)d - %(message)s'
                   ) -> logging.Logger:
    """
    配置日志记录器，可选在控制台输出，也可选择记录到日志文件。

    :param log_file: 日志文件路径，如果不为空则保存日志到文件
    :param console_output: 是否在控制台上输出日志
    :param log_level: 日志等级，默认为 'INFO'
    :param max_log_size: 最大日志文件大小（MB），默认为 10MB
    :param backup_count: 保留的备份日志文件数量，默认为 10
    :param default_log_format: 日志的默认格式
    :return: 配置后的日志记录器实例
    """
    log_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"]
    log_level = log_level if log_level.upper() in log_levels else 'INFO'

    logger = getLogger()

    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
            handler.close()

    logger.setLevel(getattr(logging, log_level.upper()))
    formatter = Formatter(default_log_format)

    if console_output:
        ch = StreamHandler()
        ch.setLevel(getattr(logging, log_level.upper()))
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True) if os.path.dirname(log_file) else None
        fh = RotatingFileHandler(log_file, maxBytes=max_log_size * 1024 * 1024, backupCount=backup_count, encoding="utf-8")
        fh.close()
        fh.setLevel(getattr(logging, log_level.upper()))
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
