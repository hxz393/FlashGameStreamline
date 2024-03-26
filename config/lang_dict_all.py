"""
语言字典
"""
LANG_DICTS = {
    'English': {
        'main_1': 'Ready',
        'main_2': '  &Start ',
        'main_3': '  &Edit  ',
        'main_5': '  &Help  ',
        'label_status_error': 'Error occurred',
        'ui.action_exit_1': 'Quit',
        'ui.action_exit_2': 'Quit the application',
        'ui.action_restore_1': 'Restore',
        'ui.action_restore_2': 'Restore Window',
        'ui.action_logs_1': 'View Logs',
        'ui.action_logs_2': 'Open Log Viewer',
        'ui.dialog_logs_1': 'View Logs',
        'ui.dialog_logs_2': 'Log Level:',
        'ui.dialog_logs_4': 'Feedback',
        'ui.dialog_logs_5': 'Clear',
        'ui.dialog_logs_6': 'Close',
        'ui.dialog_logs_7': 'Refresh',
        'ui.action_update_1': 'Check Updates',
        'ui.action_update_2': 'Check for Updates Online',
        'ui.action_update_3': 'Failed to Check for Updates!',
        'ui.action_update_4': 'New Version Available',
        'ui.action_update_5': 'No Update Needed',
        'ui.action_update_6': 'Current Version: ',
        'ui.action_update_7': 'Latest Version: ',
        'ui.action_update_8': 'Checking for Updates...',
        'ui.action_update_9': 'Update Check Complete',
        'ui.action_setting_1': 'Program Settings',
        'ui.action_setting_2': 'Open Program Settings Dialog',
        'ui.dialog_settings_main_1': 'Settings',
        'ui.dialog_settings_main_2': 'Select Language:',
        'ui.dialog_settings_main_3': 'Server Port:',
        'ui.dialog_settings_main_4': 'User Config Path:',
        'ui.dialog_settings_main_5': 'Main Settings',
        'ui.dialog_settings_main_6': 'Select',
        'ui.dialog_settings_main_11': 'Confirm',
        'ui.dialog_settings_main_12': 'Cancel',
        'ui.dialog_settings_main_13': 'Configuration Saved Successfully!',
        'ui.table_main_1': 'Active',
        'ui.table_main_2': 'Description',
        'ui.table_main_3': 'URL',
        'ui.action_enable_1': 'Enable',
        'ui.action_enable_2': 'Mark selected configuration items as enabled',
        'ui.action_enable_3': 'Items Enabled',
        'ui.action_disable_1': 'Disable',
        'ui.action_disable_2': 'Mark selected configuration items as disabled',
        'ui.action_disable_3': 'Items Disabled',
        'ui.dialog_table_1': 'Edit',
        'ui.action_add_1': 'Add',
        'ui.action_add_2': 'Add new item',
        'ui.action_add_3': 'Item Added',
        'ui.action_edit_1': 'Modify',
        'ui.action_edit_2': 'Modify item',
        'ui.action_edit_3': 'Item is Modified',
        'ui.action_delete_1': 'Delete',
        'ui.action_delete_2': 'Delete selected configuration items',
        'ui.action_delete_3': 'Items Deleted',
        'ui.action_start_1': 'Run Program',
        'ui.action_start_2': 'Start proxy server',
        'ui.action_start_3': 'Start failed, please check the rules',
        'ui.action_start_4': 'Proxy Server is Running...',
        'ui.action_start_5': 'Start failed, please change the server port',
        'ui.action_about_1': 'About',
        'ui.action_about_2': 'Information about the Software',
        'ui.dialog_about_1': 'About',
        'ui.dialog_about_2': 'Flash Game Boost Tool',
        'ui.dialog_about_3': 'Version: ',
        'ui.dialog_about_4': 'Author  :',
        'ui.dialog_about_5': 'Website :',
        'ui.dialog_about_6': 'Homepage:',
        'ui.dialog_about_7': """
                <p style="text-align: center; font-size: 16px; font-weight: bold;">Introduction</p>
                <p style="text-align: justify;">
                &nbsp;&nbsp;This tool serves as a web proxy designed to speed up Flash web games. By employing custom rules to block specific resources from downloading, it effectively enhances the games' performance.<br>
                </p>
                
                <p style="text-align: center; font-size: 16px; font-weight: bold;">Getting Help</p>
                <p style="text-align: justify;">
                &nbsp;&nbsp;Please refer to the project homepage or website for usage instructions before running. If you encounter errors during use, first check the logs for troubleshooting. For bugs and suggestions, please submit an issue on the project homepage.<br>
                </p>
                
                <p style="text-align: center; font-size: 16px; font-weight: bold;">Build Tools</p>
                <p style="text-align: justify;">
                &nbsp;&nbsp;FlashGameStreamline was built using the following tools:
                </p>
                <p><b>&nbsp;&nbsp;Program：</b>Python 3.10.4</p>
                <p><b>&nbsp;&nbsp;Interface：</b>PyQT 5.15.10</p>
                <p><b>&nbsp;&nbsp;Proxy：</b><a href='https://mitmproxy.org/'>Mitm 10.2.4</a></p>
                <p><b>&nbsp;&nbsp;Icons：</b><a href='https://icons8.com/'>icons8.com</a></p>
                """,
    },
    '中文简体': {
        'main_1': '准备就绪',
        'main_2': '开始(&S)',
        'main_3': '编辑(&E)',
        'main_5': '帮助(&H)',
        'label_status_error': '发生错误！',
        'ui.action_exit_1': '退出程序',
        'ui.action_exit_2': '立即退出程序',
        'ui.action_restore_1': '还原窗口',
        'ui.action_restore_2': '还原窗口',
        'ui.action_logs_1': '查看日志',
        'ui.action_logs_2': '打开日志文件',
        'ui.dialog_logs_1': '查看日志',
        'ui.dialog_logs_2': '日志等级：',
        'ui.dialog_logs_4': '提交反馈',
        'ui.dialog_logs_5': '清空',
        'ui.dialog_logs_6': '关闭',
        'ui.dialog_logs_7': '刷新',
        'ui.action_update_1': '检查更新',
        'ui.action_update_2': '在线检查更新',
        'ui.action_update_3': '检查更新失败！',
        'ui.action_update_4': '有新版发布',
        'ui.action_update_5': '不需要更新',
        'ui.action_update_6': '当前版本：',
        'ui.action_update_7': '最新版本：',
        'ui.action_update_8': '检查更新中...',
        'ui.action_update_9': '检查更新完成',
        'ui.action_setting_1': '程序设置',
        'ui.action_setting_2': '打开程序设置对话框',
        'ui.dialog_settings_main_1': '设置页面',
        'ui.dialog_settings_main_2': '选择语言：',
        'ui.dialog_settings_main_3': '设置代理端口：',
        'ui.dialog_settings_main_4': '用户配置文件：',
        'ui.dialog_settings_main_5': '主设置',
        'ui.dialog_settings_main_6': '选择',
        'ui.dialog_settings_main_11': '确认',
        'ui.dialog_settings_main_12': '取消',
        'ui.dialog_settings_main_13': '配置保存成功',
        'ui.table_main_1': '激活',
        'ui.table_main_2': '描述',
        'ui.table_main_3': '地址',
        'ui.action_enable_1': '启用',
        'ui.action_enable_2': '启用选择项目',
        'ui.action_enable_3': '条规则已启用',
        'ui.action_disable_1': '停用',
        'ui.action_disable_2': '停用选择项目',
        'ui.action_disable_3': '条规则已停用',
        'ui.dialog_table_1': '编辑',
        'ui.action_add_1': '新增',
        'ui.action_add_2': '新增规则',
        'ui.action_add_3': '规则已新增',
        'ui.action_edit_1': '修改',
        'ui.action_edit_2': '修改规则',
        'ui.action_edit_3': '规则已修改',
        'ui.action_delete_1': '删除',
        'ui.action_delete_2': '删除选择项目',
        'ui.action_delete_3': '条规则已删除',
        'ui.action_start_1': '启动程序',
        'ui.action_start_2': '启动代理服务器',
        'ui.action_start_3': '启动失败，无可用规则',
        'ui.action_start_4': '代理服务器运行中...',
        'ui.action_start_5': '启动失败，端口冲突，请修改代理端口设置',
        'ui.action_about_1': '关于软件',
        'ui.action_about_2': '软件相关信息',
        'ui.dialog_about_1': '关于',
        'ui.dialog_about_2': '网页游戏加速工具',
        'ui.dialog_about_3': '版本：',
        'ui.dialog_about_4': '作者：',
        'ui.dialog_about_5': '网站：',
        'ui.dialog_about_6': '主页：',
        'ui.dialog_about_7': """
                <p style="text-align: center; font-size: 16px; font-weight: bold;">程序简介</p>
                <p style="text-align: justify;">
                &nbsp;&nbsp;这是一个网络代理工具，可用于 Flash 页游加速。通过自定义规则，阻止指定资源下载，来达到运行加速效果。<br>
                </p>

                <p style="text-align: center; font-size: 16px; font-weight: bold;">获取帮助</p>
                <p style="text-align: justify;">
                &nbsp;&nbsp;运行前请查阅项目主页或网站中使用说明。如使用中遇到错误，可先查看日志自行排错。Bug 和建议请到项目主页提交 issue。<br>
                </p>

                <p style="text-align: center; font-size: 16px; font-weight: bold;">构建工具</p>
                <p style="text-align: justify;">
                &nbsp;&nbsp;FlashGameStreamline 构建用到以下工具：
                </p>
                <p><b>&nbsp;&nbsp;程序：</b>Python 3.10.4</p>
                <p><b>&nbsp;&nbsp;界面：</b>PyQT 5.15.10</p>
                <p><b>&nbsp;&nbsp;代理：</b><a href="https://mitmproxy.org/">Mitm 10.2.4</a></p>
                <p><b>&nbsp;&nbsp;图标：</b><a href="https://icons8.com/">icons8.com</a></p>
                """,
    },
}
