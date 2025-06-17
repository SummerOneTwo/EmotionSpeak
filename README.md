# EmotionSpeak - 高级情感分析与语音合成系统

> 🎭 让文本拥有情感的声音

EmotionSpeak 是一个基于深度学习的高级情感分析与智能语音合成系统，支持8种基本情感识别和智能语音参数调整。

## ✨ 核心特性

- 🎯 **多维度情感识别**: 8种基本情感 + 6种复合情感
- 🎤 **智能语音合成**: 6种语音角色，自动参数调整
- 💪 **情感强度分析**: 修饰词、标点符号、重复检测
- 🔄 **情感转折检测**: 自动识别文本中的情感变化
- 🌐 **Web界面**: 友好的用户界面和API接口
- 📊 **可视化分析**: 情感分布图表展示
- 🔒 **安全可靠**: 完善的错误处理和日志记录
- 🚀 **高性能**: 缓存优化和并发处理

## 🚀 快速开始

### 1. 环境要求
- Python 3.8+
- pip 20.0+
- Git

### 2. 一键启动（推荐）

> **注意：**
> - 如果依赖安装过程中出现 `Microsoft Visual C++ 14.0 or greater is required` 等编译环境相关报错，请先安装 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)，安装完成后重新运行脚本。

> **强烈推荐：直接运行 `start.bat`，自动完成所有初始化、依赖安装、资源下载和服务启动！**

```bat
# Windows 下双击或命令行运行
start.bat
```

- 首次运行会自动：
  - 创建并激活虚拟环境
  - 安装所有依赖
  - 创建 .env、所需目录、示例数据、文档
  - 自动下载情感分析所需词典资源
  - 启动 Web 服务并自动打开浏览器

### 3. 手动命令行方式（可选）

```sh
# 1. 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate   # Windows
# 或 source venv/bin/activate  # Linux/Mac

# 2. 一键初始化（依赖、目录、.env、资源等全部自动完成）
python init.py setup

# 3. 启动主程序
python main.py
```

- **无需手动下载任何模型或词典，所有资源自动准备。**
- 首次分析时，transformers 会自动下载 BERT 预训练模型到本地。

### 4. 访问应用

浏览器访问 [http://127.0.0.1:5000](http://127.0.0.1:5000)


## 🎭 支持的情感类型

### 基本情感
- **Joy** (喜悦): 开心、快乐、兴奋
- **Sadness** (悲伤): 难过、失落、痛苦  
- **Anger** (愤怒): 生气、恼火、暴怒
- **Fear** (恐惧): 害怕、担心、焦虑
- **Surprise** (惊讶): 意外、震惊、诧异
- **Disgust** (厌恶): 反感、嫌弃、憎恶
- **Trust** (信任): 相信、依赖、安心
- **Anticipation** (期待): 希望、憧憬、盼望

### 复合情感
- **Love** (爱): Joy + Trust
- **Hate** (恨): Anger + Disgust
- **Anxiety** (焦虑): Fear + Anticipation
- **Guilt** (内疚): Sadness + Disgust
- **Pride** (骄傲): Joy + Anger
- **Shame** (羞耻): Sadness + Fear

## 🎤 语音角色

| 角色 | 性别 | 风格 | 适合情感 |
|------|------|------|----------|
| 晓晓 | 女 | 活泼 | 喜悦、惊讶 |
| 云野 | 女 | 温暖 | 信任、爱意 |
| 晓辰 | 女 | 温和 | 信任、期待 |
| 云希 | 男 | 沉稳 | 悲伤、厌恶 |
| 云扬 | 男 | 有力 | 愤怒、兴奋 |
| 晓双 | 女 | 成熟 | 信任、严肃 |

## 💻 编程接口

### 基础使用
```python
from src.core.sentiment import SentimentAnalyzer
from src.core.tts_engine import TTSEngine

# 情感分析
analyzer = SentimentAnalyzer()
result = analyzer.analyze("今天心情特别好！")
print(f"情感: {result['emotion']['base_emotion']['label']}")
print(f"置信度: {result['emotion']['base_emotion']['confidence']}")

# 语音合成
tts = TTSEngine()
audio_path = tts.synthesize("今天心情特别好！", voice="晓晓")
```

### 高级使用
```python
from src.core.sentiment import SentimentAnalyzer

analyzer = SentimentAnalyzer()
result = analyzer.analyze_detailed("虽然今天下雨，但我还是很开心。")

print(f"主导情感: {result['emotion']['base_emotion']['label']}")
print(f"情感强度: {result['intensity']['intensity_score']:.3f}")
print(f"情感关键词: {result['emotion']['keywords']}")
```

## 📁 项目结构

```
EmotionSpeak/
├── src/
│   ├── core/
│   │   ├── sentiment/
│   │   │   ├── analyzer.py
│   │   │   ├── base.py
│   │   │   ├── dict_loader.py
│   │   │   ├── tokenizer.py
│   │   │   └── __init__.py
│   │   ├── tts_engine.py
│   │   ├── tokenizer.py
│   │   └── __init__.py
│   └── webapp/
│       ├── app.py
│       ├── config.py
│       ├── routes/
│       │   ├── api.py
│   │   │   └── __init__.py
│   │   ├── static/
│   │   │   ├── css/
│   │   │   └── js/
│   │   ├── templates/
│   │   │   └── index.html
│   │   ├── utils.py
│   │   └── __init__.py
│   ├── main.py
│   ├── init.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── start.bat
│   └── README.md
```

## 🔧 API接口

### 情感分析
```http
POST /api/analyze
Content-Type: application/json

{
  "text": "今天心情特别好！"
}
```

### 语音合成
```http
POST /api/tts
Content-Type: application/json

{
  "text": "今天心情特别好！",
  "voice": "晓晓"
}
```

## 📈 技术特点

- **多模型融合**: transformers+BERT
- **情感强度计算**: 修饰词+标点符号+重复检测  
- **智能语音选择**: 根据情感自动选择最佳语音角色
- **参数自适应**: 语速、音量根据情感强度动态调整
- **缓存优化**: 避免重复分析和合成
- **并发处理**: 支持多请求并行处理
- **错误处理**: 完善的异常捕获和日志记录
- **安全防护**: 请求限流和参数验证

## 📚 详细文档

查看 `docs/` 目录获取完整的技术文档。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

MIT License

---

**EmotionSpeak** - 让每个文本都拥有情感的声音 🎭🎵