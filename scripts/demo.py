#!/usr/bin/env python3
"""
EmotionSpeak 演示脚本
展示项目的核心功能
"""

import sys
import os
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def demo_text_processing():
    """演示文本处理功能"""
    print("\n" + "="*50)
    print("🔤 文本处理演示")
    print("="*50)
    
    try:
        from core.text_processor import TextProcessor
        
        processor = TextProcessor()
        test_texts = [
            "今天天气真好，我感到非常开心！",
            "Hello world! This is a great day.",
            "工作虽然辛苦，但是很有成就感。"
        ]
        
        for text in test_texts:
            print(f"\n原文: {text}")
            # 这里只是示例，实际实现需要根据 TextProcessor 类的接口调整
            print(f"处理后: [文本处理功能待实现]")
            
    except ImportError as e:
        print(f"⚠️  文本处理模块导入失败: {e}")

def demo_sentiment_analysis():
    """演示情感分析功能"""
    print("\n" + "="*50)
    print("😊 情感分析演示")
    print("="*50)
    
    try:
        from core.sentiment_analyzer import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        test_texts = [
            "我今天非常开心，一切都很顺利！",
            "今天工作很糟糕，心情很差。",
            "今天是普通的一天，没什么特别的。"
        ]
        
        for text in test_texts:
            print(f"\n文本: {text}")
            # 这里只是示例，实际实现需要根据 SentimentAnalyzer 类的接口调整
            print(f"情感分析: [情感分析功能待实现]")
            
    except ImportError as e:
        print(f"⚠️  情感分析模块导入失败: {e}")

def demo_tts():
    """演示语音合成功能"""
    print("\n" + "="*50)
    print("🔊 语音合成演示")
    print("="*50)
    
    try:
        from core.tts_engine import TTSEngine
        
        tts = TTSEngine()
        test_text = "欢迎使用 EmotionSpeak 情感语音系统！"
        
        print(f"正在合成语音: {test_text}")
        # 这里只是示例，实际实现需要根据 TTSEngine 类的接口调整
        print("🎵 [语音合成功能待实现]")
        
    except ImportError as e:
        print(f"⚠️  语音合成模块导入失败: {e}")

def demo_visualization():
    """演示可视化功能"""
    print("\n" + "="*50)
    print("📊 可视化演示")
    print("="*50)
    
    try:
        from visualization.wordcloud_gen import WordCloudGenerator
        from visualization.sentiment_plot import SentimentPlotter
        
        print("正在生成词云...")
        # 这里只是示例，实际实现需要根据相应类的接口调整
        print("☁️  [词云生成功能待实现]")
        
        print("\n正在生成情感趋势图...")
        print("📈 [情感趋势图功能待实现]")
        
    except ImportError as e:
        print(f"⚠️  可视化模块导入失败: {e}")

def run_comprehensive_demo():
    """运行完整演示"""
    print("🎭 EmotionSpeak 完整功能演示")
    print("="*50)
    
    # 示例文本
    sample_text = """
    今天是美好的一天！早上阳光明媚，心情特别好。
    虽然工作有些压力，但是看到项目进展顺利，还是很开心的。
    希望明天也能有这样的好心情。
    """
    
    print(f"演示文本: {sample_text.strip()}")
    
    # 运行各个功能演示
    demo_text_processing()
    demo_sentiment_analysis()
    demo_tts()
    demo_visualization()

def main():
    """主函数"""
    print("🚀 启动 EmotionSpeak 演示程序")
    
    try:
        # 检查示例文本文件
        sample_dir = Path("data/sample_texts")
        if sample_dir.exists():
            print(f"\n📁 发现示例文本目录: {sample_dir}")
            sample_files = list(sample_dir.glob("*.txt"))
            if sample_files:
                print("📄 可用的示例文件:")
                for file in sample_files:
                    print(f"   - {file.name}")
        
        # 运行演示
        run_comprehensive_demo()
        
        print("\n" + "="*50)
        print("✨ 演示完成！")
        print("\n💡 提示:")
        print("- 运行 'python main.py' 启动完整应用")
        print("- 查看 README.md 了解更多功能")
        print("- 查看 docs/ 目录获取详细文档")
        
    except KeyboardInterrupt:
        print("\n❌ 演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示运行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
