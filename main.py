# -*- coding: utf-8 -*-
"""
EmotionSpeak - 智能情感语音合成系统
主入口文件
"""

import os
import sys
import logging
from pathlib import Path

# 设置默认编码为UTF-8
if sys.platform.startswith('win'):
    import locale

    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,  # 改为DEBUG级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler('logs/app.log', encoding='utf-8'),  # 输出到文件
    ],
)
logger = logging.getLogger(__name__)

# 将 src 加入模块搜索路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def init_environment():
    """初始化环境"""
    # 确保必要的目录存在
    Path('data/audio').mkdir(parents=True, exist_ok=True)
    Path('data/models').mkdir(parents=True, exist_ok=True)
    Path('logs').mkdir(exist_ok=True)

    # 设置日志目录权限
    log_dir = Path('logs')
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)

    logger.info("环境初始化完成")


def main():
    """启动EmotionSpeak应用"""
    try:
        init_environment()

        # 导入Web应用
        from src.webapp.app import create_app
        from waitress import serve

        app = create_app()

        # 启动应用
        host = '127.0.0.1'
        port = 5000

        logger.info(f"启动EmotionSpeak Web应用 - http://{host}:{port}")
        serve(app, host=host, port=port, threads=4)

    except Exception as e:
        logger.error(f"应用启动失败: {str(e)}", exc_info=True)  # 添加完整的异常堆栈
        sys.exit(1)


if __name__ == "__main__":
    main()
