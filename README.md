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

### 使用 Makefile 命令
```bash
# 查看所有可用命令
make help

# 安装依赖
make install

# 运行主程序
make run

# 运行演示
make demo

# 运行测试
make test

# 代码格式化
make format

# 代码风格检查
make lint

# 生成测试覆盖率报告
make test-cov
```

### 直接运行
```bash
# 运行主程序
python main.py

# 运行演示程序
python scripts/demo.py
```

## 开发指南

### 代码风格
项目使用以下工具确保代码质量：
- **Black**: 代码格式化
- **Flake8**: 代码风格检查
- **pytest**: 单元测试
- **pytest-cov**: 测试覆盖率

### 提交代码前检查
```bash
# 运行所有检查
make check
```

### 测试
```bash
# 运行所有测试
make test

# 运行特定测试文件
pytest tests/test_sentiment_analyzer.py

# 生成详细的覆盖率报告
make test-cov
```

## API 文档
详细的 API 文档请参考 [API文档.md](docs/API文档.md)

## 用户指南
使用说明请参考 [用户指南.md](docs/用户指南.md)

## 依赖说明
- **pyttsx3**: 文本转语音引擎
- **textblob**: 英文文本处理和情感分析
- **nltk**: 自然语言处理工具包
- **jieba**: 中文分词
- **pygame**: 音频播放
- **wordcloud**: 词云生成
- **matplotlib**: 数据可视化
- **pillow**: 图像处理

## 贡献指南
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证
本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件

## 作者
- 开发者姓名 - [GitHub](https://github.com/username)

## 致谢
感谢所有为本项目提供帮助和建议的朋友们！

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