"""
文本预处理模块
"""

from typing import List, Dict, Any
import re
from textblob import TextBlob
from jieba import analyse
import jieba


class TextProcessor:
    """文本处理器，支持中英文混合文本的分句、标点检测、关键词提取和清理。"""

    def __init__(self):
        pass

    def clean_text(self, text: str) -> str:
        """清理文本，去除多余空格和特殊字符，保留中英文、数字和常用标点。"""
        text = re.sub(r'([!?])', r' \1 ', text)
        text = re.sub(r"[^\w\u4e00-\u9fff\s!?]", ' ', text)
        text = re.sub(r"\s+", ' ', text)
        text = text.replace('! !', '!!')
        text = re.sub(r"\s*!!", ' !!', text)
        return text.strip()

    def split_sentences(self, text: str) -> List[str]:
        """分割句子，支持中英文混合。"""
        eng_segs = re.split(r'(?<=[.!?])\s+', text)
        raw_segs = []
        for seg in eng_segs:
            parts = re.split(r'(?<=[。！？；])', seg)
            raw_segs.extend(parts)
        cleaned_segs = []
        for seg in raw_segs:
            s = self.clean_text(seg)
            if s:
                cleaned_segs.append(s)
        return cleaned_segs

    def detect_punctuation(self, sentence: str) -> dict:
        """检测句子中的常见标点数量。"""
        return {
            'exclamations': sentence.count('!'),
            'questions': sentence.count('?'),
            'ellipses': sentence.count('...'),
            'commas': sentence.count(','),
        }

    def extract_keywords(self, text: str) -> List[str]:
        """提取关键词：英文用TextBlob，中文用jieba。"""
        cleaned = self.clean_text(text)
        if re.search(r'[a-zA-Z]', cleaned) and not re.search(r'[\u4e00-\u9fff]', cleaned):
            blob = TextBlob(cleaned)
            return [word for word, tag in blob.tags if tag.startswith('NN')][:10]
        return analyse.extract_tags(cleaned, topK=10)
