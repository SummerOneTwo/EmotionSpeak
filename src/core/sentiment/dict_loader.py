"""情感词典加载器"""
import os
import json
import requests
from typing import Dict, List, Optional
from pathlib import Path

class EmotionDictLoader:
    """情感词典加载器"""
    
    # 词典下载地址
    DICT_URLS = {
        'hownet': 'https://raw.githubusercontent.com/rainarch/ChineseEmotionDictionary/master/HowNet/emotion_dict.json',
        'ntusd': 'https://raw.githubusercontent.com/rainarch/ChineseEmotionDictionary/master/NTUSD/emotion_dict.json',
        'boson': 'https://raw.githubusercontent.com/rainarch/ChineseEmotionDictionary/master/Boson/emotion_dict.json'
    }
    
    def __init__(self):
        """初始化词典加载器"""
        self.dict_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'dicts')
        os.makedirs(self.dict_dir, exist_ok=True)
        self.loaded_dicts = {}
    
    def download_dict(self, dict_name: str) -> bool:
        """下载情感词典
        
        Args:
            dict_name: 词典名称
            
        Returns:
            bool: 是否下载成功
        """
        if dict_name not in self.DICT_URLS:
            print(f"未知的词典: {dict_name}")
            return False
            
        try:
            # 下载词典
            response = requests.get(self.DICT_URLS[dict_name])
            response.raise_for_status()
            
            # 保存词典
            dict_path = os.path.join(self.dict_dir, f"{dict_name}.json")
            with open(dict_path, 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=2)
                
            print(f"词典 {dict_name} 下载成功")
            return True
            
        except Exception as e:
            print(f"词典 {dict_name} 下载失败: {str(e)}")
            return False
    
    def load_dict(self, dict_name: str) -> Optional[Dict]:
        """加载情感词典
        
        Args:
            dict_name: 词典名称
            
        Returns:
            Optional[Dict]: 词典数据
        """
        # 检查是否已加载
        if dict_name in self.loaded_dicts:
            return self.loaded_dicts[dict_name]
            
        # 检查文件是否存在
        dict_path = os.path.join(self.dict_dir, f"{dict_name}.json")
        if not os.path.exists(dict_path):
            if not self.download_dict(dict_name):
                return None
                
        try:
            # 加载词典
            with open(dict_path, 'r', encoding='utf-8') as f:
                dict_data = json.load(f)
                
            # 缓存词典
            self.loaded_dicts[dict_name] = dict_data
            return dict_data
            
        except Exception as e:
            print(f"词典 {dict_name} 加载失败: {str(e)}")
            return None
    
    def get_emotion_words(self, emotion: str) -> List[str]:
        """获取指定情感的所有词语
        
        Args:
            emotion: 情感类型
            
        Returns:
            List[str]: 情感词语列表
        """
        words = set()
        
        # 加载所有词典
        for dict_name in self.DICT_URLS.keys():
            dict_data = self.load_dict(dict_name)
            if dict_data and emotion in dict_data:
                words.update(dict_data[emotion])
                
        return list(words)
    
    def get_all_emotions(self) -> List[str]:
        """获取所有支持的情感类型
        
        Returns:
            List[str]: 情感类型列表
        """
        emotions = set()
        
        # 从所有词典中收集情感类型
        for dict_name in self.DICT_URLS.keys():
            dict_data = self.load_dict(dict_name)
            if dict_data:
                emotions.update(dict_data.keys())
                
        return list(emotions)
    
    def get_word_emotion(self, word: str) -> Dict[str, float]:
        """获取词语的情感分布
        
        Args:
            word: 输入词语
            
        Returns:
            Dict[str, float]: 情感分布字典
        """
        emotion_scores = {}
        
        # 从所有词典中收集情感分数
        for dict_name in self.DICT_URLS.keys():
            dict_data = self.load_dict(dict_name)
            if dict_data:
                for emotion, words in dict_data.items():
                    if word in words:
                        emotion_scores[emotion] = emotion_scores.get(emotion, 0) + 1
                        
        # 归一化分数
        total = sum(emotion_scores.values())
        if total > 0:
            emotion_scores = {k: v/total for k, v in emotion_scores.items()}
            
        return emotion_scores 