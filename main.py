"""
EmotionSpeak 主入口
"""

import os
import sys
import importlib

# 将 src 加入模块搜索路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

MainWindow = importlib.import_module('gui.main_window').MainWindow


def main():
    """启动EmotionSpeak GUI应用"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
