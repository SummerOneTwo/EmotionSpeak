"""
配置文件模块
"""

import json
import os

# 默认配置
DEFAULT_CONFIG = {
    "tts": {"rate": 200, "volume": 1.0, "pitch": 1.0, "voice_id": None},
    "sentiment_thresholds": {"positive": 0.1, "negative": -0.1},
    "log": {"level": "INFO", "file": "logs/app.log"},
    "output": {"dir": "data/output"},
}


def load_config(path: str) -> dict:
    """加载配置文件，若不存在或格式错误则返回默认配置"""
    if not os.path.exists(path):
        return DEFAULT_CONFIG.copy()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load config from {path}: {e}")
        return DEFAULT_CONFIG.copy()


def save_config(config: dict, path: str):
    """保存配置到指定路径（JSON）"""
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_default_config() -> dict:
    """返回一份默认配置拷贝"""
    return DEFAULT_CONFIG.copy()
