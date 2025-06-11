"""
EmotionSpeak 路由配置
"""

import os
import logging
import traceback
from pathlib import Path
from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
from core.text_processor import TextProcessor
from core.tts_engine import EdgeTTSEngine

# 创建蓝图
bp = Blueprint('main', __name__)

# 初始化处理器
text_processor = TextProcessor()
tts_engine = EdgeTTSEngine()

logger = logging.getLogger(__name__)


@bp.route('/')
def index():
    """主页"""
    return render_template('index.html')


@bp.route('/analyze', methods=['POST'])
def analyze():
    """文本分析"""
    try:
        text = request.json.get('text', '')
        if not text:
            return jsonify({'error': '请提供文本'}), 400

        logger.info(f"开始文本分析: {text}")
        # 处理文本
        result = text_processor.process(text)
        logger.info(f"文本分析完成: {result}")
        return jsonify(result)
    except Exception as e:
        error_msg = f"文本分析失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return jsonify({'error': str(e)}), 500


@bp.route('/tts', methods=['POST'])
def tts():
    """语音合成"""
    try:
        text = request.json.get('text', '')
        emotion = request.json.get('emotion', 'neutral')

        if not text:
            return jsonify({'error': '请提供文本'}), 400

        logger.info(f"开始语音合成: text={text}, emotion={emotion}")
        # 合成语音
        audio_path = tts_engine.synthesize(text, emotion)
        logger.info(f"语音合成完成: {audio_path}")

        # 验证音频文件是否存在
        full_path = Path('data/audio') / audio_path
        if not full_path.exists():
            raise Exception(f"音频文件不存在: {full_path}")

        return jsonify({'audio': audio_path})
    except Exception as e:
        error_msg = f"语音合成失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return jsonify({'error': str(e)}), 500


@bp.route('/audio/<filename>')
def get_audio(filename):
    """获取音频文件"""
    try:
        logger.info(f"请求音频文件: {filename}")
        # 使用绝对路径
        audio_dir = os.path.abspath('data/audio')
        logger.info(f"音频文件目录: {audio_dir}")

        # 验证文件是否存在
        full_path = os.path.join(audio_dir, filename)
        if not os.path.exists(full_path):
            raise Exception(f"音频文件不存在: {full_path}")

        logger.info(f"发送音频文件: {full_path}")
        return send_from_directory(audio_dir, filename)
    except Exception as e:
        error_msg = f"获取音频文件失败: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return jsonify({'error': str(e)}), 404
