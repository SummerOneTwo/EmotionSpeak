# setup.py for EmotionSpeak (可选，推荐使用 pyproject.toml)
from setuptools import setup, find_packages

setup(
    name="EmotionSpeak",
    version="0.1.0",
    description="情感语音表达与可视化工具",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyttsx3>=2.90",
        "textblob>=0.17.1",
        "nltk>=3.8",
        "pygame>=2.1.0",
        "wordcloud>=1.9.2",
        "matplotlib>=3.6.0",
        "pillow>=9.0.0",
        "jieba>=0.42.1",
    ],
)
