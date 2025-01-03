translations = {
    "window_title": "SVN文件信息导出工具",
    "svn_url": "SVN地址:",
    "username": "用户名:",
    "password": "密码:",
    "file_format_filter": "文件格式过滤",
    "file_format_placeholder": "输入文件格式，用分号分隔（例如：*.dwg;*.dxf;*.xlsx）",
    "excel_save_location": "Excel保存位置",
    "choose_path": "选择路径",
    "export_progress": "导出进度",
    "progress_format": "已处理文件进度：%v",
    "start_export": "开始导出",
    "log_info": "日志信息：",
    "validation_title": "输入验证",
    "validation_message": "以下信息未填写完整：\n",
    "warning": "警告",
    "error": "错误",
    "fill_required": "请填写所有必要信息！",
    "svn_not_found": "未检测到SVN命令行工具，请先安装TortoiseSVN并确保将命令行工具添加到系统PATH中。",
    "missing_fields": {
        "svn_url": "SVN地址",
        "username": "用户名",
        "password": "密码",
        "excel_path": "Excel保存位置"
    },
    # Log messages
    "log_parse_result": "解析结果 - 版本: {revision}, 作者: {author}, 大小: {size}, 日期时间: {date_time}, 路径: {path}",
    "log_parse_failed": "解析行失败: {line} - {error}",
    "log_executing_command": "执行SVN命令: {command}",
    "log_command_failed": "命令执行失败，返回码: {code}",
    "log_error_message": "错误信息: {error}",
    "log_command_no_output": "命令执行成功但没有输出",
    "log_command_success": "命令执行成功",
    "log_encoding_error": "编码错误，尝试使用不同的编码重新执行...",
    "log_encoding_retry_failed": "使用GBK编码重试失败: {error}",
    "log_error_occurred": "发生错误: {error}",
    "log_starting_export": "开始导出SVN信息...",
    "log_file_list_success": "成功获取SVN文件列表",
    "log_files_found": "共找到 {count} 个文件",
    "log_creating_excel": "开始创建Excel文件...",
    "log_saving_excel": "正在保存Excel文件到: {path}",
    "log_excel_saved": "Excel文件保存成功",
    "log_export_success": "成功导出 {count} 个文件信息到Excel",
    "log_svn_failed": "SVN操作失败: {error}",
    "log_program_failed": "程序执行失败: {error}",
    # Error messages
    "error_no_output": "SVN命令执行成功但没有返回任何输出，请检查URL是否正确",
    "error_encoding": "无法正确处理SVN输出的中文编码",
    "error_invalid_url": "SVN URL格式不正确，必须以 http://, https://, svn:// 或 file:/// 开头",
    "error_no_output_check": "SVN命令没有返回任何输出，请检查URL是否正确",
    "error_no_files": "未找到任何匹配的文件",
    "error_svn": "SVN错误: {error}",
    "error_general": "错误: {error}"
} 