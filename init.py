#!/usr/bin/env python3
"""
EmotionSpeak 项目初始化和演示脚本
"""

import os
import sys
import subprocess
from pathlib import Path
import shutil
import argparse

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

def install_requirements() -> None:
    """安装依赖"""
    req_file = Path('requirements.txt')
    if req_file.exists():
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        if result.returncode != 0:
            sys.exit(1)

def create_directories() -> None:
    """创建必要的目录"""
    directories = [
        'data/audio',
        'data/models',
        'data/uploads',
        'data/cache',
        'data/temp',
        'logs',
        'docs'
    ]
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True)

def copy_env_file() -> None:
    """复制环境变量模板文件"""
    env_example = Path('.env.example')
    env_file = Path('.env')
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
    elif not env_example.exists():
        env_file.write_text('FLASK_ENV=development\nFLASK_DEBUG=1\nSECRET_KEY=your-secret-key\n', encoding='utf-8')

def download_models() -> None:
    """下载预训练模型"""
    try:
        from src.core.sentiment import SentimentAnalyzer
        from src.core.tts_engine import TTSEngine
        analyzer = SentimentAnalyzer()
        tts = TTSEngine()
    except Exception as e:
        sys.exit(1)

def setup_test_data() -> None:
    """设置测试数据"""
    test_data = {
        'data/sample_texts/positive.txt': '今天天气真好，我很开心！',
        'data/sample_texts/negative.txt': '今天下雨了，心情不太好。',
        'data/sample_texts/neutral.txt': '今天是个普通的日子。',
        'data/sample_texts/mixed.txt': '虽然今天下雨，但我还是很开心。'
    }
    for file_path, content in test_data.items():
        path = Path(file_path)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')

def setup_docs() -> None:
    """设置文档"""
    doc_files = {
        'docs/installation.md': '# 安装指南\n\n## 环境要求\n\n- Python 3.8+\n- pip 20.0+\n- Git\n\n## 安装步骤\n\n1. 克隆项目\n2. 创建虚拟环境\n3. 安装依赖\n4. 配置环境\n5. 初始化项目',
        'docs/usage.md': '# 使用教程\n\n## 快速开始\n\n1. 启动应用\n2. 访问Web界面\n3. 输入文本\n4. 查看分析结果',
        'docs/api.md': '# API文档\n\n## 接口说明\n\n### 情感分析\n\n```http\nPOST /api/analyze\n```\n\n### 语音合成\n\n```http\nPOST /api/tts\n```',
        'docs/development.md': '# 开发指南\n\n## 环境设置\n\n1. 安装开发工具\n2. 配置IDE\n3. 运行测试',
        'docs/deployment.md': '# 部署指南\n\n## 生产环境\n\n1. 配置服务器\n2. 设置环境变量\n3. 启动应用',
        'docs/faq.md': '# 常见问题\n\n## 问题解答\n\n1. 如何安装？\n2. 如何使用？\n3. 如何开发？'
    }
    for file_path, content in doc_files.items():
        path = Path(file_path)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')

def init_src_resources():
    """调用 src/init_resources.py 完成资源下载"""
    import importlib.util
    resource_path = Path(__file__).parent / "src" / "init_resources.py"
    spec = importlib.util.spec_from_file_location("init_resources", resource_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.init_resources()

def main() -> None:
    parser = argparse.ArgumentParser(description='EmotionSpeak初始化脚本')
    parser.add_argument('action', choices=['setup', 'download_models', 'all'], help='要执行的操作')
    args = parser.parse_args()
    if args.action in ['setup', 'all']:
        install_requirements()
        create_directories()
        copy_env_file()
        setup_test_data()
        setup_docs()
        init_src_resources()  # 自动下载src下的资源
    if args.action in ['download_models', 'all']:
        download_models()

if __name__ == '__main__':
    main()
