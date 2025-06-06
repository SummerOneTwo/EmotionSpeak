import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class SentimentPlotView(ttk.Frame):
    """情感趋势图展示组件"""

    def __init__(self, parent):
        super().__init__(parent)
        self.figure = plt.Figure(figsize=(5, 4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.xdata = []
        self.ydata = []
        self.annotation = self.ax.annotate(
            "",
            xy=(0, 0),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"),
        )
        self.annotation.set_visible(False)
        self.canvas.mpl_connect('motion_notify_event', self._on_hover)

    def update_plot(self, polarities):
        """更新并绘制情感趋势图"""
        self.xdata = list(range(1, len(polarities) + 1))
        self.ydata = polarities
        self.ax.clear()
        self.ax.plot(self.xdata, self.ydata, marker='o', linestyle='-')
        self.ax.set_title('情感趋势')
        self.ax.set_xlabel('句子序号')
        self.ax.set_ylabel('极性值')
        self.annotation.set_visible(False)
        self.canvas.draw()

    def _on_hover(self, event):
        vis = self.annotation.get_visible()
        if event.inaxes == self.ax:
            for x, y in zip(self.xdata, self.ydata):
                if abs(event.xdata - x) < 0.1 and abs(event.ydata - y) < 0.05:
                    self.annotation.xy = (x, y)
                    text = f"{y:.2f}"
                    self.annotation.set_text(text)
                    self.annotation.set_visible(True)
                    self.canvas.draw()
                    return
        if vis:
            self.annotation.set_visible(False)
            self.canvas.draw()
