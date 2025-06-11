"""
模型下载脚本
用于下载和准备必要的模型文件
"""

import os
import sys
import logging
import requests
from tqdm import tqdm
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 模型文件配置
MODELS = {
    'bert-base-chinese': {
        'url': 'https://huggingface.co/bert-base-chinese/resolve/main/pytorch_model.bin',
        'path': 'data/models/bert-base-chinese/pytorch_model.bin',
    },
    'snownlp': {
        'url': 'https://github.com/isnowfy/snownlp/raw/master/snownlp/sentiment/sentiment.marshal',
        'path': 'data/models/snownlp/sentiment.marshal',
    },
}


def download_file(url: str, path: str):
    """
    下载文件

    Args:
        url: 文件URL
        path: 保存路径
    """
    try:
        # 创建目录
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # 下载文件
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))

        # 下载进度条
        with (
            open(path, 'wb') as f,
            tqdm(
                desc=os.path.basename(path),
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar,
        ):
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                pbar.update(size)

        logger.info(f"下载完成: {path}")

    except Exception as e:
        logger.error(f"下载失败: {str(e)}")
        raise


def main():
    """主函数"""
    try:
        # 创建必要的目录
        os.makedirs('data/models', exist_ok=True)
        os.makedirs('data/audio', exist_ok=True)

        # 下载模型文件
        for model_name, model_info in MODELS.items():
            logger.info(f"正在下载模型: {model_name}")
            download_file(model_info['url'], model_info['path'])

        logger.info("所有模型下载完成")

    except Exception as e:
        logger.error(f"模型下载失败: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
