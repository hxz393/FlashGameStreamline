"""
使用 PyInstaller 的钩子（hook）功能来确保 mitmproxy 的相关资源被正确包含在应用中
"""
from PyInstaller.utils.hooks import collect_data_files

# 收集 mitmproxy 相关的所有数据文件
datas = collect_data_files('mitmproxy')
