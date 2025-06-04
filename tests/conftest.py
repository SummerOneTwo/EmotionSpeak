import pytest
import sys
import os

# 添加源代码路径到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def sample_text():
    """提供测试用的示例文本"""
    return "今天天气真好，我感到非常开心和快乐。"

@pytest.fixture
def negative_text():
    """提供测试用的负面情感文本"""
    return "今天工作很糟糕，我感到沮丧和愤怒。"

@pytest.fixture
def neutral_text():
    """提供测试用的中性文本"""
    return "今天是星期一，我需要去上班。"

@pytest.fixture
def mixed_text():
    """提供测试用的混合情感文本"""
    return "工作虽然辛苦，但是看到成果还是很开心的。今天下雨了，心情有些低落。"
