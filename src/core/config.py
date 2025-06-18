import os

# 获取 config.py 的上两级目录（即 src/ 的上一级 = 项目根目录）
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(DATA_DIR, 'models')
AUDIO_DIR = os.path.join(DATA_DIR, 'audio')
DICTS_DIR = os.path.join(DATA_DIR, 'dicts')
UPLOADS_DIR = os.path.join(DATA_DIR, 'uploads')
STOPWORDS_PATH = os.path.join(DATA_DIR, 'stopwords.txt')

# 你可以根据需要继续添加其他路径 