"""中文分词模块"""
from typing import List, Dict
import jieba_fast as jieba
import jieba_fast.posseg as pseg
import os

class ChineseTokenizer:
    """中文分词器"""
    
    def __init__(self):
        """初始化分词器，自动加载自定义词典和停用词表（如存在）"""
        dict_path = os.path.join(os.path.dirname(__file__), 'data', 'jieba_dict.txt')
        stopwords_path = os.path.join(os.path.dirname(__file__), 'data', 'stopwords.txt')
        # 加载自定义词典
        if os.path.exists(dict_path):
            jieba.load_userdict(dict_path)
        # 加载停用词表
        self.stopwords = set()
        if os.path.exists(stopwords_path):
            with open(stopwords_path, encoding='utf-8') as f:
                self.stopwords = set(line.strip() for line in f if line.strip())
    
    def tokenize(self, text: str) -> List[Dict]:
        """分词并标注词性，自动过滤停用词"""
        words_info = []
        for word, flag in pseg.cut(text):
            if word not in self.stopwords:
                words_info.append({
                    'word': word,
                    'nature': flag
                })
        return words_info
    
    def get_words(self, text: str) -> List[str]:
        """只获取分词结果，不包含词性，自动过滤停用词"""
        return [word for word, _ in pseg.cut(text) if word not in self.stopwords]
    
    def add_word(self, word: str, freq: int = None, tag: str = None):
        """添加自定义词
        
        Args:
            word: 要添加的词
            freq: 词频
            tag: 词性
        """
        jieba.add_word(word, freq, tag)
    
    def load_dict(self, dict_path: str):
        """加载自定义词典
        
        Args:
            dict_path: 词典文件路径
        """
        jieba.load_userdict(dict_path) 