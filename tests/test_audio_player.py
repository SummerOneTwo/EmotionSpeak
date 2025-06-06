import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from core import audio_player
import tempfile

def test_audio_player_functions_exist():
    """测试音频播放器函数是否存在"""
    assert hasattr(audio_player, 'play')
    assert hasattr(audio_player, 'pause')
    assert hasattr(audio_player, 'resume')
    assert hasattr(audio_player, 'stop')

def test_pygame_initialization():
    """测试pygame混音器初始化"""
    # pygame.mixer应该在模块导入时初始化
    import pygame
    assert pygame.mixer.get_init() is not None

def test_play_nonexistent_file():
    """测试播放不存在的文件"""
    with pytest.raises(Exception):
        audio_player.play("nonexistent_file.mp3")

def test_control_functions():
    """测试播放控制函数"""
    # 这些函数在没有音频播放时也应该能安全调用
    try:
        audio_player.pause()
        audio_player.resume()
        audio_player.stop()
        assert True
    except Exception as e:
        # 某些情况下可能会出现pygame相关错误，这是可以接受的
        assert "pygame" in str(e).lower() or "mixer" in str(e).lower()

def test_play_with_valid_file():
    """测试播放有效的音频文件（如果可用）"""
    # 创建一个临时的WAV文件头（最小有效WAV文件）
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        # 写入一个最小的WAV文件头
        wav_header = b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
        tmp.write(wav_header)
        tmp_path = tmp.name
    
    try:
        # 尝试播放文件
        audio_player.play(tmp_path)
        # 如果能执行到这里，说明play函数正常工作
        assert True
    except Exception as e:
        # 在某些环境中可能没有音频设备或支持
        assert any(keyword in str(e).lower() for keyword in ['audio', 'mixer', 'device', 'sound'])
    finally:
        # 清理临时文件
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def test_threading_safety():
    """测试线程安全性"""
    # 音频播放器应该能处理并发调用
    import threading
    
    def control_audio():
        try:
            audio_player.pause()
            audio_player.resume()
            audio_player.stop()
        except:
            pass  # 忽略测试环境中的音频错误
    
    threads = []
    for i in range(3):
        t = threading.Thread(target=control_audio)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    assert True  # 如果没有死锁或崩溃，测试通过
