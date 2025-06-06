"""
情感趋势图模块
"""

import matplotlib.pyplot as plt
from typing import List


class SentimentPlotter:
    """情感趋势图生成器"""

    def plot_sentiment_trend(self, sentiments: List[float], output_path: str, **kwargs) -> bool:
        """绘制情感趋势图"""
        plt.figure(figsize=kwargs.get('figsize', (8, 4)))
        plt.plot(sentiments, marker='o')
        plt.title('Sentiment Trend')
        plt.xlabel('Sentence')
        plt.ylabel('Polarity')
        plt.savefig(output_path)
        plt.close()
        return True

    def plot_emotion_distribution(self, emotions: dict, output_path: str) -> bool:
        """绘制情感分布饼图"""
        plt.figure(figsize=(6, 6))
        plt.pie(emotions.values(), labels=emotions.keys(), autopct='%1.1f%%')
        plt.title('Emotion Distribution')
        plt.savefig(output_path)
        plt.close()
        return True
