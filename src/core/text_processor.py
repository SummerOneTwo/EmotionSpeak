"""
文本处理模块
"""

import jieba
import snownlp
from typing import Dict, List


class TextProcessor:
    """文本处理器"""

    def __init__(self):
        """初始化文本处理器"""
        # 加载停用词
        self.stopwords = set()
        try:
            with open('data/stopwords.txt', 'r', encoding='utf-8') as f:
                self.stopwords = set(line.strip() for line in f)
        except FileNotFoundError:
            pass

    def process(self, text: str) -> Dict:
        """处理文本"""
        # 分词
        words = list(jieba.cut(text))

        # 去除停用词
        words = [w for w in words if w not in self.stopwords]

        # 情感分析
        sentiment = snownlp.SnowNLP(text)

        # 提取关键词
        keywords = self._extract_keywords(words)

        return {
            'words': words,
            'sentiment': {'score': sentiment.sentiments, 'emotion': self._get_emotion(sentiment.sentiments)},
            'keywords': keywords,
        }

    def _extract_keywords(self, words: List[str]) -> List[str]:
        """提取关键词"""
        # 简单的词频统计
        word_freq = {}
        for word in words:
            if len(word) > 1:  # 只考虑长度大于1的词
                word_freq[word] = word_freq.get(word, 0) + 1

        # 按频率排序
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in keywords[:5]]  # 返回前5个关键词

    def _get_emotion(self, score: float) -> str:
        """根据情感分数获取情感标签"""
        if score > 0.6:
            return 'happy'
        elif score < 0.4:
            return 'sad'
        else:
            return 'neutral'
