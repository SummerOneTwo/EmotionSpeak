# -*- coding: utf-8 -*-
"""
EmotionSpeak Web应用
"""

from flask import Flask
from flask_cors import CORS


def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    CORS(app)

    # 注册路由
    from .routes import bp

    app.register_blueprint(bp)

    return app
