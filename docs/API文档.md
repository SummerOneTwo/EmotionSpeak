# EmotionSpeak API 文档

## 目录
- [文本预处理](#文本预处理)
- [情感分析](#情感分析)
- [语音合成](#语音合成)
- [音频播放](#音频播放)
- [可视化](#可视化)
- [GUI组件](#gui组件)
- [配置管理](#配置管理)
- [工具函数](#工具函数)

---

## 文本预处理

### `TextProcessor` 类

#### 方法

##### `clean_text(text: str) -> str`
清理和规范化输入文本。

**参数:**
- `text` (str): 需要清理的原始文本

**返回:**
- `str`: 清理后的文本

**示例:**
```python
from src.core.text_processor import TextProcessor

processor = TextProcessor()
clean_text = processor.clean_text("Hello!!! World???")
# 返回: "Hello! World?"
```

##### `tokenize(text: str, lang: str = 'zh') -> List[str]`
对文本进行分词处理。

**参数:**
- `text` (str): 待分词的文本
- `lang` (str): 语言类型，'zh' 为中文，'en' 为英文

**返回:**
- `List[str]`: 分词结果列表

**示例:**
```python
tokens = processor.tokenize("今天天气真好", lang='zh')
# 返回: ["今天", "天气", "真", "好"]
```

##### `preprocess(text: str, lang: str = 'zh') -> Dict[str, Any]`
综合预处理文本，包括清理和分词。

**参数:**
- `text` (str): 原始文本
- `lang` (str): 语言类型

**返回:**
- `Dict[str, Any]`: 包含原文、清理后文本、分词结果等信息的字典

---

## 情感分析

### `SentimentAnalyzer` 类

#### 方法

##### `analyze_sentiment(text: str, lang: str = 'zh') -> Dict[str, Any]`
分析文本的情感倾向。

**参数:**
- `text` (str): 待分析的文本
- `lang` (str): 文本语言

**返回:**
- `Dict[str, Any]`: 情感分析结果
  ```python
  {
      'sentiment': 'positive',  # 情感极性: positive/negative/neutral
      'score': 0.85,           # 情感强度分数 [-1.0, 1.0]
      'confidence': 0.92,      # 置信度 [0.0, 1.0]
      'emotions': {            # 具体情感分布
          'joy': 0.7,
          'anger': 0.1,
          'sadness': 0.1,
          'fear': 0.1
      }
  }
  ```

##### `batch_analyze(texts: List[str], lang: str = 'zh') -> List[Dict[str, Any]]`
批量分析多个文本的情感。

**参数:**
- `texts` (List[str]): 文本列表
- `lang` (str): 文本语言

**返回:**
- `List[Dict[str, Any]]`: 情感分析结果列表

---

## 语音合成

### `TTSEngine` 类

#### 方法

##### `speak(text: str, emotion: str = None, save_path: str = None) -> bool`
将文本转换为语音并播放或保存。

**参数:**
- `text` (str): 待转换的文本
- `emotion` (str, optional): 情感类型 ('happy', 'sad', 'angry', 'neutral')
- `save_path` (str, optional): 保存音频文件的路径

**返回:**
- `bool`: 操作是否成功

##### `set_voice_properties(rate: int = None, volume: float = None) -> None`
设置语音属性。

**参数:**
- `rate` (int): 语音速度 (50-300)
- `volume` (float): 音量 (0.0-1.0)

##### `get_available_voices() -> List[Dict[str, str]]`
获取可用的语音引擎列表。

**返回:**
- `List[Dict[str, str]]`: 可用语音列表

---

## 音频播放

### `AudioPlayer` 类

#### 方法

##### `play(audio_path: str) -> bool`
播放指定的音频文件。

**参数:**
- `audio_path` (str): 音频文件路径

**返回:**
- `bool`: 播放是否成功

##### `stop() -> None`
停止当前播放的音频。

##### `pause() -> None`
暂停当前播放的音频。

##### `resume() -> None`
恢复播放暂停的音频。

---

## 可视化

### `WordCloudGenerator` 类

#### 方法

##### `generate_wordcloud(words: List[str], output_path: str, **kwargs) -> bool`
生成词云图片。

**参数:**
- `words` (List[str]): 词语列表
- `output_path` (str): 输出图片路径
- `**kwargs`: 其他自定义参数
  - `width` (int): 图片宽度，默认 800
  - `height` (int): 图片高度，默认 600
  - `background_color` (str): 背景颜色，默认 'white'

**返回:**
- `bool`: 生成是否成功

### `SentimentPlotter` 类

#### 方法

##### `plot_sentiment_trend(sentiments: List[float], output_path: str, **kwargs) -> bool`
绘制情感趋势图。

**参数:**
- `sentiments` (List[float]): 情感分数序列
- `output_path` (str): 输出图片路径
- `**kwargs`: 其他自定义参数

**返回:**
- `bool`: 绘制是否成功

##### `plot_emotion_distribution(emotions: Dict[str, float], output_path: str) -> bool`
绘制情感分布饼图。

**参数:**
- `emotions` (Dict[str, float]): 情感分布数据
- `output_path` (str): 输出图片路径

**返回:**
- `bool`: 绘制是否成功

---

## GUI组件

### `MainWindow` 类

主窗口类，提供图形用户界面。

#### 方法

##### `__init__(self)`
初始化主窗口。

##### `run(self) -> None`
启动GUI应用程序。

---

## 配置管理

### `Config` 类

#### 属性

- `TTS_RATE`: TTS语音速度
- `TTS_VOLUME`: TTS音量
- `DEFAULT_LANGUAGE`: 默认语言
- `OUTPUT_DIR`: 输出目录
- `FONT_PATH`: 字体文件路径

#### 方法

##### `load_config(config_path: str = None) -> Dict[str, Any]`
加载配置文件。

##### `save_config(config: Dict[str, Any], config_path: str = None) -> bool`
保存配置到文件。

---

## 工具函数

### `helpers.py`

##### `ensure_dir(path: str) -> None`
确保目录存在，如不存在则创建。

##### `get_file_encoding(file_path: str) -> str`
检测文件编码格式。

##### `safe_filename(filename: str) -> str`
生成安全的文件名。

---

## 错误处理

所有API方法都包含适当的错误处理机制。常见错误类型：

- `TextProcessError`: 文本处理错误
- `SentimentAnalysisError`: 情感分析错误
- `TTSError`: 语音合成错误
- `AudioError`: 音频播放错误
- `VisualizationError`: 可视化生成错误

## 使用示例

### 完整流程示例

```python
from src.core import TextProcessor, SentimentAnalyzer, TTSEngine
from src.visualization import WordCloudGenerator

# 1. 文本预处理
processor = TextProcessor()
text = "今天天气真好，我感到非常开心！"
processed = processor.preprocess(text)

# 2. 情感分析
analyzer = SentimentAnalyzer()
sentiment = analyzer.analyze_sentiment(text)

# 3. 语音合成
tts = TTSEngine()
tts.speak(text, emotion=sentiment['sentiment'])

# 4. 可视化
wordcloud_gen = WordCloudGenerator()
wordcloud_gen.generate_wordcloud(
    processed['tokens'], 
    'output/wordcloud.png'
)
```
