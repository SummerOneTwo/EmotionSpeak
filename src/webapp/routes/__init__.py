"""
路由模块
"""

from flask import Blueprint
from .api import api_bp

def register_routes(app):
    """注册路由
    
    Args:
        app: Flask应用实例
    """
    # 注册蓝图
    app.register_blueprint(api_bp, url_prefix='/api') 