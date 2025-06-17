"""
Web应用配置
"""

import os
from typing import Dict, Any

class Config:
    """基础配置"""
    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    DEBUG = False
    TESTING = False
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 会话配置
    PERMANENT_SESSION_LIFETIME = 3600  # 1小时
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'app.log')
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
    
    # API配置
    API_TITLE = 'EmotionSpeak API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_SWAGGER_UI_PATH = '/swagger-ui'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    OPENAPI_REDOC_PATH = '/redoc'
    OPENAPI_REDOC_URL = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'
    
    # 情感分析配置
    SENTIMENT_ANALYSIS = {
        'max_text_length': 1000,
        'min_text_length': 1,
        'confidence_threshold': 0.6,
        'emotion_threshold': 0.3,
        'intensity_levels': {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
    }
    
    # 语音合成配置
    TTS_CONFIG = {
        'default_voice': 'zh-CN-XiaoxiaoNeural',
        'default_style': 'cheerful',
        'default_pitch': 1.0,
        'default_speed': 1.0,
        'default_volume': 1.0,
        'output_format': 'mp3',
        'sample_rate': 24000
    }
    
    # 缓存配置
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # 跨域配置
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']
    CORS_METHODS = ['GET', 'POST', 'OPTIONS']
    CORS_HEADERS = ['Content-Type', 'Authorization']
    
    # 限流配置
    RATELIMIT_DEFAULT = '200 per day;50 per hour'
    RATELIMIT_STORAGE_URL = 'memory://'
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """获取当前环境的配置"""
        env = os.environ.get('FLASK_ENV', 'development')
        return config[env]

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    SESSION_COOKIE_SECURE = False
    CORS_ORIGINS = ['*']
    RATELIMIT_DEFAULT = '1000 per day;100 per hour'

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    LOG_LEVEL = 'DEBUG'
    SESSION_COOKIE_SECURE = False
    CORS_ORIGINS = ['*']
    RATELIMIT_DEFAULT = '1000 per day;100 per hour'

class ProductionConfig(Config):
    """生产环境配置"""
    LOG_LEVEL = 'WARNING'
    SESSION_COOKIE_SECURE = True
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    RATELIMIT_DEFAULT = '100 per day;10 per hour'

# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 