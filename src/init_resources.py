"""
资源初始化脚本
下载和准备情感分析所需的资源（与 core 兼容）
"""

import os
import json
import requests
from pathlib import Path
from tqdm import tqdm

# 资源目录
RESOURCE_DIR = Path(__file__).parent.parent / 'data'
DICT_DIR = RESOURCE_DIR / 'dicts'

# 情感词典下载地址（与 core/sentiment/dict_loader.py 保持一致）
DICT_URLS = {
    'hownet': 'https://raw.githubusercontent.com/rainarch/ChineseEmotionDictionary/master/HowNet/emotion_dict.json',
    'ntusd': 'https://raw.githubusercontent.com/rainarch/ChineseEmotionDictionary/master/NTUSD/emotion_dict.json',
    'boson': 'https://raw.githubusercontent.com/rainarch/ChineseEmotionDictionary/master/Boson/emotion_dict.json'
}

def download_file(url: str, save_path: Path, desc: str = None):
    """下载文件（带进度条）"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    with open(save_path, 'wb') as f, tqdm(
        desc=desc or save_path.name,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(block_size):
            size = f.write(data)
            pbar.update(size)

def init_directories():
    """初始化目录结构"""
    RESOURCE_DIR.mkdir(parents=True, exist_ok=True)
    DICT_DIR.mkdir(parents=True, exist_ok=True)

def download_dictionaries():
    """下载情感词典（HowNet/NTUSD/Boson）"""
    for name, url in DICT_URLS.items():
        save_path = DICT_DIR / f"{name}.json"
        if not save_path.exists():
            print(f"下载词典: {name}")
            download_file(url, save_path)
    print("情感词典下载完成")

def init_resources():
    """初始化所有资源"""
    print("开始初始化资源...")
    init_directories()
    download_dictionaries()
    print("资源初始化完成")

if __name__ == '__main__':
    init_resources() 