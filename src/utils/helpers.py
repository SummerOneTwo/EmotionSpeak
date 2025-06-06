"""
辅助函数模块
"""

import os
import logging
import chardet


def ensure_dir(path: str):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def safe_filename(filename: str) -> str:
    """生成安全的文件名"""
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()


def get_file_encoding(file_path: str) -> str:
    """检测文件编码格式"""
    with open(file_path, 'rb') as f:
        raw = f.read(4096)
    result = chardet.detect(raw)
    return result['encoding'] or 'utf-8'


def init_logger(log_file: str = 'logs/app.log', level: int = logging.INFO):
    """初始化日志系统"""
    ensure_dir(os.path.dirname(log_file))
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        handlers=[logging.FileHandler(log_file, encoding='utf-8'), logging.StreamHandler()],
    )
