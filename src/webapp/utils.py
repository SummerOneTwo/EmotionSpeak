"""
Web应用工具
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from flask import current_app, request, jsonify
from werkzeug.utils import secure_filename

def get_error_response(message: str, code: int = 400) -> Tuple[Dict[str, Any], int]:
    """获取错误响应
    
    Args:
        message: 错误信息
        code: HTTP状态码
        
    Returns:
        错误响应字典和状态码
    """
    return {
        'success': False,
        'error': {
            'message': message,
            'code': code,
            'timestamp': datetime.now().isoformat()
        }
    }, code

def get_success_response(data: Optional[Dict[str, Any]] = None, message: Optional[str] = None) -> Dict[str, Any]:
    """获取成功响应
    
    Args:
        data: 响应数据
        message: 成功信息
        
    Returns:
        成功响应字典
    """
    response = {
        'success': True,
        'timestamp': datetime.now().isoformat()
    }
    if data is not None:
        response['data'] = data
    if message is not None:
        response['message'] = message
    return response

def allowed_file(filename: str) -> bool:
    """检查文件是否允许上传
    
    Args:
        filename: 文件名
        
    Returns:
        是否允许上传
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file) -> Optional[str]:
    """保存上传的文件
    
    Args:
        file: 文件对象
        
    Returns:
        保存的文件路径，如果保存失败则返回None
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 添加时间戳和哈希值，避免文件名冲突
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        hash_value = hashlib.md5(f"{name}{timestamp}".encode()).hexdigest()[:8]
        filename = f"{name}_{timestamp}_{hash_value}{ext}"
        
        # 确保上传目录存在
        upload_dir = current_app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        return file_path
    return None

def get_client_ip() -> str:
    """获取客户端IP地址
    
    Returns:
        客户端IP地址
    """
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

def format_datetime(dt: datetime) -> str:
    """格式化日期时间
    
    Args:
        dt: 日期时间对象
        
    Returns:
        格式化后的日期时间字符串
    """
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def format_timedelta(td) -> str:
    """格式化时间间隔
    
    Args:
        td: 时间间隔对象
        
    Returns:
        格式化后的时间间隔字符串
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}" 