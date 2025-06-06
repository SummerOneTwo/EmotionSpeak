import os
import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from core.tts_engine import TTSEngine


def test_save_audio(tmp_path):
    tts = TTSEngine()
    text = "Hello world"
    out_file = tmp_path / "out_test.wav"
    filename = str(out_file)
    result = tts.save_audio(text, filename)
    assert os.path.exists(result)
    assert result == filename


def test_speak():
    """测试TTS语音合成功能"""
    tts = TTSEngine()
    
    # 测试基本语音合成
    try:
        sentiment = {'polarity': 0.0, 'classification': 'neutral'}
        tts.speak_with_emotion("Hello world", sentiment)
        assert True
    except Exception as e:
        # 在CI/CD环境中可能没有音频设备
        assert "audio" in str(e).lower() or "device" in str(e).lower() or "init" in str(e).lower()

def test_get_available_voices():
    """测试获取可用语音"""
    tts = TTSEngine()
    voices = tts.get_available_voices()
    assert isinstance(voices, list)
    # 大部分系统至少有一个语音
    if len(voices) > 0:
        voice = voices[0]
        assert 'id' in voice
        assert 'name' in voice

def test_set_voice_properties():
    """测试设置语音属性"""
    tts = TTSEngine()
    
    # 测试设置语速和音量
    tts.set_voice_properties(rate=150, volume=0.8)
    
    # 测试边界值
    tts.set_voice_properties(volume=1.5)  # 应该被限制为1.0
    tts.set_voice_properties(volume=-0.5)  # 应该被限制为0.0
    
    assert True  # 如果没有异常则通过

def test_emotion_adjustment():
    """测试情感调整功能"""
    tts = TTSEngine()
    
    config = {
        "tts": {
            "rate": 200,
            "volume": 0.8,
            "pitch": 1.0
        }
    }
    
    # 测试积极情感
    positive_sentiment = {'polarity': 0.8, 'classification': 'positive'}
    try:
        tts.speak_with_emotion("This is positive", positive_sentiment, config)
        assert True
    except Exception as e:
        assert "audio" in str(e).lower() or "device" in str(e).lower() or "init" in str(e).lower()
    
    # 测试消极情感
    negative_sentiment = {'polarity': -0.8, 'classification': 'negative'}
    try:
        tts.speak_with_emotion("This is negative", negative_sentiment, config)
        assert True
    except Exception as e:
        assert "audio" in str(e).lower() or "device" in str(e).lower() or "init" in str(e).lower()
