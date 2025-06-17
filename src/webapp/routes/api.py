"""
API路由
处理API接口的路由
"""

from flask import Blueprint, request, jsonify, send_file
from ...core import SentimentAnalyzer, TTSEngine

# 创建蓝图
api_bp = Blueprint('api', __name__)

# 创建分析器和TTS引擎实例
sentiment_analyzer = SentimentAnalyzer()
tts_engine = TTSEngine()

@api_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    result = sentiment_analyzer.analyze(data['text'])
    return jsonify({'success': True, 'result': result})

@api_bp.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    auto_analyze = data.get('auto_analyze', True)
    try:
        output_file = tts_engine.synthesize_with_emotion(data['text'], auto_analyze=auto_analyze)
        return jsonify({
            'success': True,
            'audio_url': f'/audio/{output_file.split("/")[-1]}'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/audio/<filename>')
def get_audio(filename):
    return send_file(f'data/audio/{filename}')

@api_bp.route('/voices')
def get_voices():
    return jsonify({
        'success': True,
        'voices': tts_engine.get_available_voices()
    }) 