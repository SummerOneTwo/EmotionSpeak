"""
主窗口模块
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from core.text_processor import TextProcessor
from core.sentiment_analyzer import SentimentAnalyzer
from core.tts_engine import TTSEngine
from visualization.wordcloud_view import WordCloudView
from visualization.sentiment_plot_view import SentimentPlotView


class MainWindow:
    """主窗口类（待实现）"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EmotionSpeak")
        self.root.geometry("1000x700")
        self.processor = TextProcessor()
        self.analyzer = SentimentAnalyzer()
        self.tts = TTSEngine()

        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(top_frame, text="输入文本：").pack(anchor='nw')
        self.text_input = tk.Text(top_frame, height=10)
        self.text_input.pack(fill='x')

        control_frame = ttk.Frame(top_frame)
        control_frame.pack(fill='x', pady=5)
        ttk.Label(control_frame, text="情感模式：").pack(side='left')
        self.mode_var = tk.StringVar(value="自动")
        self.mode_cb = ttk.Combobox(
            control_frame,
            textvariable=self.mode_var,
            values=("自动", "积极", "消极"),
            state='readonly',
            width=10,
        )
        self.mode_cb.pack(side='left', padx=5)

        ttk.Button(control_frame, text="播放", command=self.on_play).pack(side='left', padx=5)
        ttk.Button(control_frame, text="保存音频", command=self.on_save).pack(side='left', padx=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        wc_frame = ttk.Frame(self.notebook)
        sp_frame = ttk.Frame(self.notebook)
        self.notebook.add(wc_frame, text="词云")
        self.notebook.add(sp_frame, text="情感趋势")

        self.wordcloud_view = WordCloudView(wc_frame)
        self.wordcloud_view.pack(fill='both', expand=True)
        self.plot_view = SentimentPlotView(sp_frame)
        self.plot_view.pack(fill='both', expand=True)

    def run(self):
        self.root.mainloop()

    def on_play(self):
        text = self.text_input.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("提示", "请输入文本")
            return
        import threading

        threading.Thread(target=self._process_and_play, args=(text,), daemon=True).start()

    def _process_and_play(self, text):
        try:
            sentences = self.processor.split_sentences(text)
            sentiments = self.analyzer.batch_analyze(sentences)
            if self.mode_var.get() == "自动":
                avg = sum([s['polarity'] for s in sentiments]) / len(sentiments)
                cls = self.analyzer.classify_emotion(avg)
                overall = {'polarity': avg, 'classification': cls}
            else:
                mapping = {"积极": "positive", "消极": "negative"}
                cls = mapping.get(self.mode_var.get(), 'neutral')
                overall = {'polarity': 0, 'classification': cls}

            self.tts.speak_with_emotion(text, overall)

            keywords = self.processor.extract_keywords(text)
            self.wordcloud_view.update_keywords(keywords)
            polarities = [s['polarity'] for s in sentiments]
            self.plot_view.update_plot(polarities)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def on_save(self):
        text = self.text_input.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("提示", "请输入文本")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV", "*.wav")])
        if not filename:
            return
        import threading

        threading.Thread(target=self._save_audio, args=(text, filename), daemon=True).start()

    def _save_audio(self, text, filename):
        try:
            sentences = self.processor.split_sentences(text)
            sentiments = self.analyzer.batch_analyze(sentences)
            if self.mode_var.get() == "自动":
                avg = sum([s['polarity'] for s in sentiments]) / len(sentiments)
                cls = self.analyzer.classify_emotion(avg)
                overall = {'polarity': avg, 'classification': cls}
            else:
                mapping = {"积极": "positive", "消极": "negative"}
                cls = mapping.get(self.mode_var.get(), 'neutral')
                overall = {'polarity': 0, 'classification': cls}

            self.tts.save_audio(text, filename, overall)
            messagebox.showinfo("成功", f"音频已保存到 {filename}")
        except Exception as e:
            messagebox.showerror("错误", str(e))
