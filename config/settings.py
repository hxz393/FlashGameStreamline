"""
全局静态变量
"""
# 配置路径
CONFIG_MAIN_PATH = 'config/config_main.json'
LOG_PATH = 'logs/run.log'
# 程序信息
PROGRAM_NAME = 'FlashGameStreamline'
VERSION_INFO = 'v1.0.0'
AUTHOR_NAME = 'assassing'
CONTACT_MAIL = 'hxz393@gmail.com'
WEBSITE_URL = 'https://blog.x2b.net'
CHECK_UPDATE_URL = 'https://blog.x2b.net/ver/flashgamestreamline.txt'
GITHUB_PROFILE = 'https://github.com/hxz393'
GITHUB_URL = 'https://github.com/hxz393/FlashGameStreamline'
# 默认配置
DEFAULT_CONFIG_MAIN = {
    'lang': 'English',  # zh-cht en zh-chs
    'server_port': '12345',
    'config_user_path': 'config/config_user.json',
}
DEFAULT_CONFIG_USER = {
    "url": {
        "active": False,
        "description": "",
    }
}
# 用户输入检查正则
REGEX_PORT = r'^\d{1,5}$'
REGEX_ASCII = r'^[ -~]+$'
# 日志弹窗配置
LOG_DEFAULT_LEVEL = '--ALL--'
LOG_COLORS = {
    "DEBUG": "gray",
    "INFO": "black",
    "WARNING": "orange",
    "ERROR": "red",
    "CRITICAL": "darkred"
}
LOG_LEVELS = [i for i in LOG_COLORS.keys()]
# 日志展示最多行数
LOG_LINES = 1000
# 日志定时刷新毫秒数
LOG_UPDATE_RATE = 200
