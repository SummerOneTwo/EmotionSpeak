"""
Web应用模块
提供Web界面和API接口
"""

from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes import register_routes

def create_app(config_class=Config):
    """创建Flask应用实例
    
    Args:
        config_class: 配置类
        
    Returns:
        Flask应用实例
    """
    # 创建应用实例
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    CORS(app)
    
    # 注册路由
    register_routes(app)
    
    return app 