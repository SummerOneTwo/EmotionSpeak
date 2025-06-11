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
        self.emotion_keywords = {
            'positive': [
                '开心',
                '高兴',
                '快乐',
                '喜悦',
                '满意',
                '兴奋',
                '愉快',
                '好',
                '棒',
                '太棒了',
                '完美',
                '优秀',
            ],
            'negative': [
                '难过',
                '伤心',
                '痛苦',
                '愤怒',
                '生气',
                '沮丧',
                '失望',
                '糟糕',
                '烦躁',
                '焦虑',
                '担心',
            ],
            'neutral': ['普通', '一般', '平常', '正常', '还好', '可以'],
        }

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """分析单句情感，英文用TextBlob，中文用SnowNLP"""
        try:
            # 预处理文本
            text = text.strip()
            if not text:
                return {'polarity': 0.0, 'confidence': 0.0}

            # 检测是否包含中文
            if re.search(r'[\u4e00-\u9fff]', text):
                # 中文情感分析
                s = SnowNLP(text)
                polarity = s.sentiments * 2 - 1  # 转换到 [-1, 1] 范围

                # 基于关键词增强情感检测
                keyword_score = self._keyword_sentiment_score(text)
                polarity = (polarity + keyword_score) / 2

                confidence = abs(polarity)
            else:
                # 英文情感分析
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                confidence = abs(polarity)

            return {
                'polarity': polarity,
                'confidence': confidence,
                'classification': self.classify_emotion(polarity),
            }
        except Exception as e:
            print(f"情感分析失败: {e}")
            return {'polarity': 0.0, 'confidence': 0.0, 'classification': 'neutral'}

    def _keyword_sentiment_score(self, text: str) -> float:
        """基于关键词计算情感分数"""
        score = 0.0
        text_lower = text.lower()

        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if emotion == 'positive':
                        score += 0.3
                    elif emotion == 'negative':
                        score -= 0.3

        return max(-1.0, min(1.0, score))  # 限制在 [-1, 1] 范围

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
