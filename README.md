# EmotionSpeak - 智能情感语音合成系统

EmotionSpeak 是一个基于 Python 的智能情感语音合成系统，能够分析文本情感并生成相应的语音。

## 功能特点

- 文本情感分析
- 智能语音合成
- 支持多种情感表达
- 基于微软 Edge TTS 服务
- 完全免费，无需 API 密钥

## 系统要求

- Python 3.8 或更高版本
- Windows 操作系统

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/EmotionSpeak.git
cd EmotionSpeak
```

2. 创建虚拟环境：
```bash
python -m venv .venv
```

3. 激活虚拟环境：
```bash
# Windows
.venv\Scripts\activate
```

4. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

1. 启动应用：
```bash
python main.py
```

2. 在浏览器中访问：
```
http://127.0.0.1:5000
```

3. 输入文本，点击"分析文本"按钮进行情感分析
4. 点击"合成语音"按钮生成语音

## 项目结构

```
EmotionSpeak/
├── src/                    # 源代码目录
│   ├── core/              # 核心功能模块
│   └── webapp/            # Web应用模块
├── data/                  # 数据目录
│   ├── audio/            # 音频文件
│   └── models/           # 模型文件
├── logs/                  # 日志目录
├── main.py               # 主程序入口
├── requirements.txt      # 依赖列表
└── README.md            # 项目说明
```

## 许可证

MIT License

## 作者

[您的名字]