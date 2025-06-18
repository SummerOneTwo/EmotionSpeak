"""情感词典加载器"""
import os
import json
import requests
from typing import Dict, List, Optional
from pathlib import Path
from ..config import DICTS_DIR

class EmotionDictLoader:
    """情感词典加载器"""
    
    # 可用的词典列表
    AVAILABLE_DICTS = ['hownet', 'thu', 'ntusd', 'boson']
    
    def __init__(self):
        """初始化词典加载器"""
        self.loaded_dicts = {}
        # 优先查找项目根目录 data/dicts
        self.dict_dir = DICTS_DIR
        os.makedirs(self.dict_dir, exist_ok=True)
        if os.path.exists(self.dict_dir):
            pass
    
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
        
        # 只检查 DICTS_DIR 下的文件
        dict_path = os.path.join(self.dict_dir, f"{dict_name}.json")
        
        if not os.path.exists(dict_path):
            return None
        
        try:
            # 加载词典
            with open(dict_path, 'r', encoding='utf-8') as f:
                dict_data = json.load(f)
                
            # 缓存词典
            self.loaded_dicts[dict_name] = dict_data
            return dict_data
            
        except Exception as e:
            return None
    
    def get_emotion_words(self, emotion: str) -> List[str]:
        """获取指定情感的所有词语
        
        Args:
            emotion: 情感类型
            
        Returns:
            List[str]: 情感词语列表
        """
        words = set()
        
        # 从所有词典中收集词语
        for dict_name in self.AVAILABLE_DICTS:
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
        for dict_name in self.AVAILABLE_DICTS:
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
        dict_weights = {
            'hownet': 1.0,   # 知网词典权重
            'thu': 0.8,      # 清华词典权重
            'ntusd': 0.8,    # 台大词典权重
            'boson': 1.0     # Boson词典权重
        }
        
        # 从所有词典中收集情感分数
        for dict_name in self.AVAILABLE_DICTS:
            dict_data = self.load_dict(dict_name)
            if dict_data:
                weight = dict_weights.get(dict_name, 1.0)
                for emotion, words in dict_data.items():
                    if word in words:
                        emotion_scores[emotion] = emotion_scores.get(emotion, 0) + weight
                        
        # 归一化分数
        total = sum(emotion_scores.values())
        if total > 0:
            emotion_scores = {k: v/total for k, v in emotion_scores.items()}
            
        return emotion_scores 