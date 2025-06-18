import os
import sys
import subprocess
import shutil
import argparse
import importlib.util
from transformers import AutoTokenizer, AutoModelForSequenceClassification

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
DICT_DIR = os.path.join(DATA_DIR, 'dicts')
AUDIO_DIR = os.path.join(DATA_DIR, 'audio')
UPLOADS_DIR = os.path.join(DATA_DIR, 'uploads')
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, 'requirements.txt')

def install_requirements():
    print('[init] 安装依赖...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', REQUIREMENTS_FILE])

def setup_essential_dirs():
    print('[init] 创建必要目录...')
    os.makedirs(DICT_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(UPLOADS_DIR, exist_ok=True)

def check_dicts():
    print('[init] 检查情感词典...')
    required_dicts = ['hownet.json', 'thu.json', 'ntusd.json', 'boson.json']
    missing = []
    if not os.path.exists(DICT_DIR):
        os.makedirs(DICT_DIR, exist_ok=True)
    for dict_file in required_dicts:
        dict_path = os.path.join(DICT_DIR, dict_file)
        if not os.path.exists(dict_path):
            missing.append(dict_file)
    if missing:
        print(f'[WARNING] 缺少以下情感词典文件: {missing}')
        print(f'请将四个 json 词典文件放置到 {DICT_DIR} 后重试。')
        # Create empty dict files to avoid errors
        for dict_file in missing:
            with open(os.path.join(DICT_DIR, dict_file), 'w', encoding='utf-8') as f:
                f.write('{}')
        print('[init] 已创建空词典文件，程序可以继续运行，但情感分析效果可能受影响。')
    else:
        print('[init] 情感词典已就绪！')

def copy_env_file():
    """复制环境变量配置文件"""
    print('[init] 检查环境变量配置...')
    env_example = os.path.join(PROJECT_ROOT, '.env.example')
    env_file = os.path.join(PROJECT_ROOT, '.env')
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        shutil.copy(env_example, env_file)
        print('[init] 已创建 .env 文件')
    elif not os.path.exists(env_file) and not os.path.exists(env_example):
        # Create a basic .env file
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write('# EmotionSpeak 环境配置\n')
            f.write('HOST=127.0.0.1\n')
            f.write('PORT=5000\n')
            f.write('FLASK_ENV=development\n')
        print('[init] 已创建基础 .env 文件')
    else:
        print('[init] .env 文件已存在')

def download_model():
    print('[init] 检查情感分析模型...')
    cache_dir = os.path.join(DATA_DIR, 'models')
    os.makedirs(cache_dir, exist_ok=True)
    model_prefix = 'models--IDEA-CCNL--Erlangshen-Roberta-330M-Sentiment'
    found = False
    required_files = ['config.json', 'vocab.txt']
    model_files = ['pytorch_model.bin', 'model.safetensors']
    for d in os.listdir(cache_dir):
        if d.startswith(model_prefix):
            model_dir = os.path.join(cache_dir, d, 'snapshots')
            # print(f'[DEBUG] 检查目录: {model_dir}')
            if os.path.exists(model_dir):
                for snap in os.listdir(model_dir):
                    snap_dir = os.path.join(model_dir, snap)
                    # print(f'[DEBUG] 检查快照: {snap_dir}')
                    files = os.listdir(snap_dir)
                    # print(f'[DEBUG] 快照文件: {files}')
                    if all(f in files for f in required_files) and any(f in files for f in model_files):
                        found = True
                        break
    if found:
        print('[init] 情感分析模型已存在，无需重复下载。')
        return
    print('[init] 下载情感分析模型...')
    try:
        AutoTokenizer.from_pretrained(
            "IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",
            cache_dir=cache_dir,
            local_files_only=False
        )
        AutoModelForSequenceClassification.from_pretrained(
            "IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",
            cache_dir=cache_dir,
            local_files_only=False
        )
        print('[init] 模型下载完成！')
    except Exception as e:
        print(f'[WARNING] 模型下载失败: {str(e)}')
        print('[init] 将使用备用模型进行情感分析')

def download_models():
    check_dicts()
    download_model()
    print('[init] 资源全部就绪！')

def main():
    parser = argparse.ArgumentParser(description='EmotionSpeak初始化脚本')
    parser.add_argument('action', choices=['setup', 'download_models', 'all'], help='要执行的操作')
    args = parser.parse_args()
    if args.action == 'setup':
        install_requirements()
        copy_env_file()
        setup_essential_dirs()
    elif args.action == 'download_models':
        check_dicts()
        download_model()
        print('[init] 资源全部就绪！')
    elif args.action == 'all':
        install_requirements()
        setup_essential_dirs()
        copy_env_file()
        check_dicts()
        download_model()
        print('[init] 所有依赖和资源已准备完毕！')

if __name__ == '__main__':
    main() 