"""
词云生成模块
"""

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import List


class WordCloudGenerator:
    """词云生成器"""

    def __init__(self, font_path: str = None):
        self.font_path = font_path

    def generate_wordcloud(
        self,
        words: List[str],
        output_path: str,
        width: int = 800,
        height: int = 600,
        background_color: str = 'white',
    ) -> bool:
        """生成词云图片"""
        text = ' '.join(words)
        wc = WordCloud(
            font_path=self.font_path, width=width, height=height, background_color=background_color
        )
        wc.generate(text)
        wc.to_file(output_path)
        return True
