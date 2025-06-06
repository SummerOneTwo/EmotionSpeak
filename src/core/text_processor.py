"""
文本预处理模块
"""

from typing import List
import re
from textblob import TextBlob
from jieba import analyse
import jieba

def clean_text(text: str) -> str:
    """清理文本，去除非中英文字符并合并空格"""
    # 在感叹号和问号两侧添加空格，方便保留并分离
    text = re.sub(r'([!?])', r' \1 ', text)
    # 保留感叹号和问号，其他非中英文字符替换为空格
    text = re.sub(r"[^\w\u4e00-\u9fff\s!?]", ' ', text)
    text = re.sub(r"\s+", ' ', text)
    # 合并分离的连续感叹号为紧凑形式，并保证前有一个空格
    text = text.replace('! !', '!!')
    text = re.sub(r"\s*!!", ' !!', text)
    return text.strip()

def split_sentences(text: str) -> List[str]:
    """分割句子，支持中英文混合"""
    # 英文简单分句，匹配 .!? 后跟空格
    eng_segs = re.split(r'(?<=[.!?])\s+', text)
    # 针对每个英文分句，再按中文标点分割
    raw_segs = []
    for seg in eng_segs:
        parts = re.split(r'(?<=[。！？；])', seg)
        raw_segs.extend(parts)
    # 清理并收集非空句子
    cleaned_segs = []
    for seg in raw_segs:
        s = clean_text(seg)
        if s:
            cleaned_segs.append(s)
    return cleaned_segs

def detect_punctuation(sentence: str) -> dict:
    """检测句子中的常见标点数量"""
    return {
        'exclamations': sentence.count('!'),
        'questions': sentence.count('?'),
        'ellipses': sentence.count('...'),
        'commas': sentence.count(','),
    }

def extract_keywords(text: str) -> List[str]:
    """提取关键词：英文基于POS标注，中文基于TF-IDF"""
    cleaned = clean_text(text)
    # 纯英文
    if re.search(r'[a-zA-Z]', cleaned) and not re.search(r'[\u4e00-\u9fff]', cleaned):
        blob = TextBlob(cleaned)
        return [word for word, tag in blob.tags if tag.startswith('NN')][:10]
    # 中文或混合，以中文关键词为主
    return analyse.extract_tags(cleaned, topK=10)

class TextProcessor:
    """文本处理器封装类"""
    def __init__(self):
        pass

    def clean_text(self, text: str) -> str:
        return clean_text(text)

    def split_sentences(self, text: str) -> List[str]:
        return split_sentences(text)

    def detect_punctuation(self, sentence: str) -> dict:
        return detect_punctuation(sentence)

    def extract_keywords(self, text: str) -> List[str]:
        return extract_keywords(text)
