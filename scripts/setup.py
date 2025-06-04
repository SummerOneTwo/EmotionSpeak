#!/usr/bin/env python3
"""
EmotionSpeak 项目初始化脚本
用于设置项目环境和下载必要的资源
"""

import os
import sys
import subprocess
import nltk
from pathlib import Path

def setup_nltk_data():
    """下载必要的 NLTK 数据"""
    print("正在下载 NLTK 数据...")
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        print("✅ NLTK 数据下载完成")
    except Exception as e:
        print(f"❌ NLTK 数据下载失败: {e}")

def create_directories():
    """创建必要的目录"""
    print("正在创建项目目录...")
    directories = [
        "data/output",
        "data/sample_texts",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def create_sample_texts():
    """创建示例文本文件"""
    print("正在创建示例文本...")
    
    sample_texts = {
        "positive.txt": "今天天气真好，我感到非常开心和快乐！阳光明媚，心情愉悦。",
        "negative.txt": "今天工作很糟糕，我感到沮丧和愤怒。一切都不顺利，心情很差。",
        "neutral.txt": "今天是星期一，我需要去上班。会议安排在下午两点开始。",
        "mixed.txt": "工作虽然辛苦，但是看到成果还是很开心的。今天下雨了，心情有些低落，但是团队合作很愉快。"
    }
    
    for filename, content in sample_texts.items():
        filepath = Path("data/sample_texts") / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 创建示例文件: {filepath}")

def check_system_dependencies():
    """检查系统依赖"""
    print("正在检查系统依赖...")
    
    # 检查 espeak (Linux 系统)
    if sys.platform.startswith('linux'):
        try:
            subprocess.run(['espeak', '--version'], 
                         capture_output=True, check=True)
            print("✅ espeak 已安装")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  espeak 未安装，请运行: sudo apt-get install espeak espeak-data")
    
    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("❌ Python 版本过低，需要 Python 3.8 或更高版本")
        sys.exit(1)
    else:
        print(f"✅ Python 版本: {sys.version}")

def main():
    """主函数"""
    print("🚀 EmotionSpeak 项目初始化开始...")
    print("=" * 50)
    
    try:
        check_system_dependencies()
        create_directories()
        create_sample_texts()
        setup_nltk_data()
        
        print("=" * 50)
        print("🎉 项目初始化完成！")
        print("\n接下来你可以:")
        print("1. 运行 'make run' 启动主程序")
        print("2. 运行 'make demo' 查看演示")
        print("3. 运行 'make test' 执行测试")
        print("4. 查看 README.md 了解更多信息")
        
    except KeyboardInterrupt:
        print("\n❌ 初始化被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
