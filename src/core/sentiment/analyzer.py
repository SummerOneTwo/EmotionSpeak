"""中文情感分析器"""
import torch
import os
from typing import Dict, List, Optional, Union
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertTokenizer, BertForSequenceClassification
from .base import BASIC_EMOTIONS, COMPOUND_EMOTIONS, INTENSITY_MODIFIERS
from ..tokenizer import ChineseTokenizer
from .tokenizer import EmotionTokenizer

# 全局模型缓存
_MODEL_CACHE = {
    'model': None,
    'tokenizer': None,
    'is_initialized': False
}

class SentimentAnalyzer:
    """中文情感分析器"""
    
    def __init__(self):
        """初始化情感分析器"""
        self._is_initialized = False
        self.model = None
        self.word_tokenizer = None
        self.tokenizer = EmotionTokenizer()
        
    def _initialize(self):
        """初始化模型"""
        if self._is_initialized:
            return
            
        try:
            # 检查全局缓存
            global _MODEL_CACHE
            if not _MODEL_CACHE['is_initialized']:
                print("正在加载情感分析模型...")
                # 设置模型缓存目录
                cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'models')
                os.makedirs(cache_dir, exist_ok=True)
                
                # 初始化BERT模型 - 使用最新的Erlangshen模型
                _MODEL_CACHE['tokenizer'] = AutoTokenizer.from_pretrained(
                    "IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",
                    local_files_only=False,  # 允许从网络下载
                    cache_dir=cache_dir     # 使用绝对路径
                )
                _MODEL_CACHE['model'] = AutoModelForSequenceClassification.from_pretrained(
                    "IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",
                    local_files_only=False,
                    cache_dir=cache_dir
                )
                _MODEL_CACHE['is_initialized'] = True
                print("模型加载完成！")
            
            # 初始化分词器
            self.word_tokenizer = ChineseTokenizer()
            self._is_initialized = True
            
        except Exception as e:
            print(f"模型加载失败: {str(e)}")
            self._cleanup()  # 清理资源
            raise RuntimeError(f"情感分析器初始化失败: {str(e)}")
    
    def _cleanup(self):
        """清理资源"""
        self.word_tokenizer = None
        self._is_initialized = False
    
    def __del__(self):
        """析构函数，确保资源被正确释放"""
        self._cleanup()
    
    def analyze(self, text: str) -> Dict:
        """分析文本情感
        
        Args:
            text: 输入文本
            
        Returns:
            Dict: 情感分析结果
            
        Raises:
            RuntimeError: 当模型未正确初始化时
            ValueError: 当输入文本为空或无效时
        """
        if not text or not isinstance(text, str):
            raise ValueError("输入文本不能为空且必须是字符串类型")
            
        if not self._is_initialized or not _MODEL_CACHE['is_initialized']:
            raise RuntimeError("情感分析器未正确初始化，请检查模型加载状态")
            
        try:
            # 使用BERT分析基础情感
            inputs = _MODEL_CACHE['tokenizer'](text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = _MODEL_CACHE['model'](**inputs)
                scores = torch.softmax(outputs.logits, dim=1)[0]
                
            # 获取基础情感标签和置信度
            base_emotion_idx = scores.argmax().item()
            base_confidence = scores[base_emotion_idx].item()
            
            # 分析情感强度
            intensity = self._analyze_intensity(text)
            
            # 使用分词器进行分词
            words_info = self.word_tokenizer.tokenize(text)
            
            # 分析复合情感
            compound_emotions = self._analyze_compound_emotions(text)
            
            # 分析情感关键词
            emotion_keywords = self._analyze_emotion_keywords(text)
            
            return {
                'text': text,
                'emotion': {
                    'base_emotion': {
                        'label': '正面' if base_emotion_idx == 1 else '负面',
                        'confidence': base_confidence,
                        'score': scores[1].item()
                    },
                    'compound_emotions': compound_emotions,
                    'keywords': emotion_keywords
                },
                'intensity': intensity,
                'words': words_info
            }
            
        except Exception as e:
            print(f"情感分析失败: {str(e)}")
            return self._get_error_result(text, str(e))
    
    def _get_error_result(self, text: str, error_msg: str) -> Dict:
        """获取错误情况下的默认结果
        
        Args:
            text: 输入文本
            error_msg: 错误信息
            
        Returns:
            Dict: 默认分析结果
        """
        return {
            'text': text,
            'error': error_msg,
            'emotion': {
                'base_emotion': {
                    'label': '未知',
                    'confidence': 0.0,
                    'score': 0.0
                },
                'compound_emotions': [],
                'keywords': {}
            },
            'intensity': {
                'intensity_score': 1.0,
                'modifiers': [],
                'has_repetition': False
            },
            'words': []
        }
    
    def _analyze_intensity(self, text: str) -> Dict:
        """分析情感强度
        
        Args:
            text: 输入文本
            
        Returns:
            Dict: 情感强度分析结果
        """
        try:
            # 检查修饰词
            intensity_score = 1.0
            modifiers = []
            for modifier, factor in INTENSITY_MODIFIERS.items():
                if modifier in text:
                    intensity_score *= factor
                    modifiers.append(modifier)
            
            # 检查标点符号
            if '！' in text or '!' in text:
                intensity_score *= 1.2
            if '？' in text or '?' in text:
                intensity_score *= 0.9
                
            # 检查重复
            words = self.word_tokenizer.get_words(text)
            has_repetition = any(words[i] == words[i+1] for i in range(len(words)-1))
            if has_repetition:
                intensity_score *= 1.1
                    
            return {
                'intensity_score': min(max(intensity_score, 0.1), 2.0),
                'modifiers': modifiers,
                'has_repetition': has_repetition
            }
            
        except Exception as e:
            print(f"情感强度分析失败: {str(e)}")
            return {
                'intensity_score': 1.0,
                'modifiers': [],
                'has_repetition': False
            }
    
    def _analyze_compound_emotions(self, text: str) -> List[Dict]:
        """分析复合情感
        
        Args:
            text: 输入文本
            
        Returns:
            List[Dict]: 复合情感列表
        """
        try:
            compound_emotions = []
            for emotion_id, emotion_info in COMPOUND_EMOTIONS.items():
                # 检查关键词
                if any(keyword in text for keyword in emotion_info['keywords']):
                    # 计算基础情感得分
                    base_scores = []
                    for component in emotion_info['components']:
                        if any(keyword in text for keyword in BASIC_EMOTIONS[component]['keywords']):
                            base_scores.append(1.0)
                        else:
                            base_scores.append(0.0)
                    
                    if base_scores:
                        compound_emotions.append({
                            'label': emotion_info['label'],
                            'components': emotion_info['components'],
                            'confidence': sum(base_scores) / len(base_scores)
                        })
            
            return compound_emotions
            
        except Exception as e:
            print(f"复合情感分析失败: {str(e)}")
            return []
    
    def _analyze_emotion_keywords(self, text: str) -> Dict[str, List[str]]:
        """分析情感关键词
        
        Args:
            text: 输入文本
            
        Returns:
            Dict[str, List[str]]: 情感关键词映射
        """
        try:
            emotion_keywords = {}
            
            # 分析基本情感关键词
            for emotion_id, emotion_info in BASIC_EMOTIONS.items():
                found_keywords = [keyword for keyword in emotion_info['keywords'] if keyword in text]
                if found_keywords:
                    emotion_keywords[emotion_info['label']] = found_keywords
            
            # 分析复合情感关键词
            for emotion_id, emotion_info in COMPOUND_EMOTIONS.items():
                found_keywords = [keyword for keyword in emotion_info['keywords'] if keyword in text]
                if found_keywords:
                    emotion_keywords[emotion_info['label']] = found_keywords
            
            return emotion_keywords
            
        except Exception as e:
            print(f"情感关键词分析失败: {str(e)}")
            return {}
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """批量分析文本情感
        
        Args:
            texts: 输入文本列表
            
        Returns:
            List[Dict]: 情感分析结果列表
            
        Raises:
            ValueError: 当输入列表为空或包含无效文本时
        """
        if not texts or not isinstance(texts, list):
            raise ValueError("输入文本列表不能为空且必须是列表类型")
            
        return [self.analyze(text) for text in texts]
    
    def analyze_compound(self, text: str) -> Dict[str, float]:
        """分析复合情感
        
        Args:
            text: 输入文本
            
        Returns:
            Dict[str, float]: 复合情感分析结果
        """
        # 获取基础情感分数
        base_scores = self.analyze(text)
        if not base_scores:
            return {}
            
        # 计算复合情感分数
        compound_scores = {}
        for compound, components in COMPOUND_EMOTIONS.items():
            score = 0.0
            for emotion, weight in components.items():
                if emotion in base_scores:
                    score += base_scores[emotion] * weight
            compound_scores[compound] = score
            
        return compound_scores
    
    def analyze_intensity(self, text: str) -> float:
        """分析情感强度
        
        Args:
            text: 输入文本
            
        Returns:
            float: 情感强度分数
        """
        # 获取情感词
        emotion_words = self.tokenizer.get_emotion_words(text)
        if not emotion_words:
            return 0.0
            
        # 计算情感强度
        intensity = 0.0
        for word, _ in emotion_words:
            word_emotions = self.tokenizer.get_word_emotion(word)
            intensity += sum(word_emotions.values())
            
        # 归一化强度
        return min(1.0, intensity / len(emotion_words))
    
    def analyze_keywords(self, text: str) -> List[Dict[str, Union[str, float]]]:
        """分析情感关键词
        
        Args:
            text: 输入文本
            
        Returns:
            List[Dict[str, Union[str, float]]]: 情感关键词列表
        """
        # 获取情感词
        emotion_words = self.tokenizer.get_emotion_words(text)
        if not emotion_words:
            return []
            
        # 计算每个词的情感分数
        keywords = []
        for word, emotion in emotion_words:
            word_emotions = self.tokenizer.get_word_emotion(word)
            if word_emotions:
                max_emotion = max(word_emotions.items(), key=lambda x: x[1])
                keywords.append({
                    'word': word,
                    'emotion': max_emotion[0],
                    'score': max_emotion[1]
                })
                
        # 按分数排序
        keywords.sort(key=lambda x: x['score'], reverse=True)
        return keywords
    
    def analyze_detailed(self, text: str) -> Dict:
        """详细情感分析
        
        Args:
            text: 输入文本
            
        Returns:
            Dict: 详细分析结果
        """
        return {
            'emotions': self.analyze(text),
            'compound_emotions': self.analyze_compound(text),
            'intensity': self.analyze_intensity(text),
            'keywords': self.analyze_keywords(text)
        } 