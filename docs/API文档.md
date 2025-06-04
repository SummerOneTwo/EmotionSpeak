# EmotionSpeak API 文档

## 目录
- 文本预处理
- 情感分析
- 语音合成
- 音频播放
- 可视化

---

## 文本预处理
### `text_processor.py`
- `clean_text(text: str) -> str`
  - 文本清洗，去除特殊字符。
- `tokenize(text: str, lang: str = 'zh') -> List[str]`
  - 分词，支持中英文。

## 情感分析
### `sentiment_analyzer.py`
- `analyze_sentiment(text: str, lang: str = 'zh') -> Dict`
  - 返回情感分数与极性。

## 语音合成
### `tts_engine.py`
- `speak(text: str, emotion: str = None)`
  - 按指定情感合成语音。

## 音频播放
### `audio_player.py`
- `play(audio_path: str)`
  - 播放指定音频文件。

## 可视化
### `wordcloud_gen.py`
- `generate_wordcloud(words: List[str], output_path: str)`
  - 生成词云图片。

### `sentiment_plot.py`
- `plot_sentiment_trend(sentiments: List[float], output_path: str)`
  - 绘制情感趋势图。
