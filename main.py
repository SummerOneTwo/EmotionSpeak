# -*- coding: utf-8 -*-
"""
EmotionSpeak - 智能情感语音合成系统
主入口文件
"""

import os
import sys
from pathlib import Path
from waitress import serve
from src.webapp.app import create_app

# 设置默认编码为UTF-8
if sys.platform.startswith('win'):
    import locale
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')

# 将 src 加入模块搜索路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def main():
    """主程序入口"""
    # 创建应用
    app = create_app()
    # 获取配置
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', 5000))
    # 启动服务器
    serve(app, host=host, port=port)

if __name__ == '__main__':
    main()
