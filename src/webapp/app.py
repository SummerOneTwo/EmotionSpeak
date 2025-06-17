# -*- coding: utf-8 -*-
"""
EmotionSpeak Web应用
"""

import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from .config import config
from .routes import register_routes
from ..core.sentiment import SentimentAnalyzer
from ..core.tts_engine import TTSEngine

# 加载环境变量
load_dotenv()

def create_app(config_name: str = 'default') -> Flask:
    """创建并配置Flask应用
    
    Args:
        config_name: 配置名称
        
    Returns:
        Flask应用实例
    """
    # 创建应用实例
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    CORS(app)
    
    # 初始化情感分析器
    sentiment_analyzer = SentimentAnalyzer()
    app.sentiment_analyzer = sentiment_analyzer
    
    # 初始化TTS引擎
    tts_engine = TTSEngine()
    app.tts_engine = tts_engine
    
    # 注册路由
    register_routes(app)
    
    @app.route('/')
    def index():
        """主页"""
        return render_template('index.html')
    
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        """提供静态文件"""
        return send_from_directory(app.static_folder, filename)
    
    @app.route('/audio/<path:filename>')
    def serve_audio(filename):
        """提供音频文件"""
        audio_dir = os.path.join(os.getcwd(), 'data', 'audio')
        return send_from_directory(audio_dir, filename)
    
    @app.route('/health')
    def health_check():
        """健康检查"""
        return jsonify({
            'status': 'healthy',
            'version': '2.0.0',
        })
    
    return app

def get_app() -> Flask:
    """获取应用实例
    
    Returns:
        Flask应用实例
    """
    env = os.environ.get('FLASK_ENV', 'default')
    return create_app(env)

if __name__ == "__main__":
    app = get_app()
    app.run(
        host=os.environ.get('FLASK_HOST', '0.0.0.0'),
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    )
