import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class WordCloudView(ttk.Frame):
    """词云展示组件"""

    def __init__(self, parent):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(5, 4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill='x')
        refresh_btn = ttk.Button(btn_frame, text="刷新词云", command=self._on_refresh)
        refresh_btn.pack(pady=5)
        self.keywords = []

    def _on_refresh(self):
        self.update_keywords(self.keywords)

    def update_keywords(self, keywords):
        """更新并绘制词云"""
        self.keywords = keywords
        self.ax.clear()
        if keywords:
            text = ' '.join(keywords)
            wc = WordCloud(font_path=None, background_color='white').generate(text)
            self.ax.imshow(wc, interpolation='bilinear')
            self.ax.axis('off')
        self.canvas.draw()
