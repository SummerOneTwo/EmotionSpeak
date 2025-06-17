"""
EmotionSpeak 核心模块
提供情感分析和语音合成功能
"""

from .sentiment_analysis import SentimentAnalyzer
from .tts_engine import TTSEngine

# 可选导入音频播放器（如果pygame可用）
try:
    from .audio_player import AudioPlayer

    _audio_available = True
except ImportError:
    AudioPlayer = None
    _audio_available = False

__all__ = [
    'SentimentAnalyzer',
    'TTSEngine',
]

if _audio_available:
    __all__.append('AudioPlayer')

__version__ = "2.0.0"
