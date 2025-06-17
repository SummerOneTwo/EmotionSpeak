"""情感分析分词器"""
import jieba_fast as jieba
import jieba_fast.posseg as pseg
from typing import List, Dict, Tuple
from .dict_loader import EmotionDictLoader

class EmotionTokenizer:
    """情感分析分词器"""
    
    def __init__(self):
        """初始化分词器"""
        # 加载情感词典
        self.dict_loader = EmotionDictLoader()
        self._load_emotion_dicts()
        
    def _load_emotion_dicts(self):
        """加载情感词典到jieba"""
        # 加载所有情感词典
        for dict_name in self.dict_loader.DICT_URLS.keys():
            dict_data = self.dict_loader.load_dict(dict_name)
            if dict_data:
                for emotion, words in dict_data.items():
                    for word in words:
                        jieba.add_word(word, tag=f'emotion_{emotion}')
    
    def tokenize(self, text: str) -> List[Tuple[str, str]]:
        """分词并标注词性
        
        Args:
            text: 输入文本
            
        Returns:
            List[Tuple[str, str]]: 词语和词性标注列表
        """
        # 使用jieba进行分词和词性标注
        words = pseg.cut(text)
        return [(word, flag) for word, flag in words]
    
    def get_emotion_words(self, text: str) -> List[Tuple[str, str]]:
        """获取文本中的情感词
        
        Args:
            text: 输入文本
            
        Returns:
            List[Tuple[str, str]]: 情感词和情感类型列表
        """
        words = self.tokenize(text)
        emotion_words = []
        
        for word, flag in words:
            if flag.startswith('emotion_'):
                emotion = flag.split('_')[1]
                emotion_words.append((word, emotion))
                
        return emotion_words
    
    def get_word_emotion(self, word: str) -> Dict[str, float]:
        """获取词语的情感分布
        
        Args:
            word: 输入词语
            
        Returns:
            Dict[str, float]: 情感分布字典
        """
        return self.dict_loader.get_word_emotion(word)
    
    def get_all_emotions(self) -> List[str]:
        """获取所有支持的情感类型
        
        Returns:
            List[str]: 情感类型列表
        """
        return self.dict_loader.get_all_emotions() 