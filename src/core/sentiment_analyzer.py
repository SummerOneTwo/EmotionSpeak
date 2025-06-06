"""
情感分析模块
"""

from typing import List, Dict
from snownlp import SnowNLP
from textblob import TextBlob
import re


class SentimentAnalyzer:
    def __init__(self):
        """初始化情感分析器"""
        pass

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """分析单句情感，英文用TextBlob，中文用SnowNLP。"""
        if re.search(r'[\u4e00-\u9fff]', text):
            s = SnowNLP(text)
            polarity = s.sentiments * 2 - 1
        else:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
        return {'polarity': polarity}

    def classify_emotion(self, polarity: float) -> str:
        """情感分类。"""
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        return 'neutral'

    def batch_analyze(self, sentences: List[str]) -> List[Dict[str, float]]:
        """批量分析情感。"""
        results = []
        for s in sentences:
            res = self.analyze_sentiment(s)
            res['classification'] = self.classify_emotion(res['polarity'])
            results.append(res)
        return results


# 保持向后兼容的函数接口
def analyze_sentiment(text: str, lang: str = 'zh'):
    """返回情感分数与极性。"""
    analyzer = SentimentAnalyzer()
    return analyzer.analyze_sentiment(text)


def classify_emotion(polarity: float) -> str:
    """根据polarity分类情感"""
    analyzer = SentimentAnalyzer()
    return analyzer.classify_emotion(polarity)


def batch_analyze(sentences: List[str]) -> List[Dict[str, float]]:
    """对句子列表批量情感分析"""
    analyzer = SentimentAnalyzer()
    return analyzer.batch_analyze(sentences)
