# **EmotionSpeak**

### Rationale
- **Emotion**: Highlights the project's core feature of emotional analysis using NLP to adjust TTS output for expressive reading.
- **Speak**: Emphasizes the Text-to-Speech (TTS) functionality, which converts text into spoken language with dynamic tone and cadence.
- **Fit for Purpose**: The name is concise, memorable, and reflects the integration of emotional analysis and speech synthesis, aligning with the project's innovative aspects and the course's focus on AI and Python programming.

---

## 项目简介
EmotionSpeak 是一个集文本情感分析、语音合成（TTS）、音频播放与可视化为一体的工具，适用于中文和英文文本。

## 主要功能
- 文本预处理与分词
- 情感分析（支持中英文）
- 语音合成与播放
- 词云与情感趋势可视化
- 简洁易用的图形界面

## 目录结构
```
EmotionSpeak/
├── src/
│   ├── core/
│   ├── gui/
│   ├── visualization/
│   └── utils/
├── tests/
├── data/
├── docs/
├── scripts/
├── requirements.txt
├── pyproject.toml
├── main.py
└── .gitignore
```

## 环境配置
1. **克隆项目**
   ```bash
   git clone <repo-url>
   cd EmotionSpeak
   ```
2. **创建虚拟环境**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

## 快速开始
```bash
make run
```
或
```bash
python main.py
```

## 代码格式化与检查
```bash
make format
make lint
```

## 测试
```bash
make test
```

## 文档
- [API文档](docs/API文档.md)
- [用户指南](docs/用户指南.md)

## 许可证
MIT License