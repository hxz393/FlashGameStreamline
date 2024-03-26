"""
此模块用于展示弹出窗口。

:author: assassing
:contact: https://github.com/hxz393
:copyright: Copyright 2024, hxz393. 保留所有权利。
"""

import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from lib.get_resource_path import get_resource_path

logger = logging.getLogger(__name__)


def message_show(message_type: str,
                 text: str) -> None:
    """
    显示指定类型的消息框。

    :param message_type: 消息类型，支持 'Critical'、'Warning' 和 'Information'。
    :param text: 消息框中显示的纯文本内容。
    :return: 无返回值。
    """
    try:
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setWindowTitle(message_type)

        if message_type == 'Critical':
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowIcon(QIcon(get_resource_path('media/icons8-error-26')))
        elif message_type == 'Warning':
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowIcon(QIcon(get_resource_path('media/icons8-do-not-disturb-26')))
        elif message_type == 'Information':
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowIcon(QIcon(get_resource_path('media/icons8-about-26')))
        else:
            logger.warning("Invalid message type provided.")

        msg_box.exec_()
    except Exception:
        logger.exception("An error occurred while displaying the message box")
