"""中文情感分析器"""
import torch
import os
from typing import Dict, List, Optional, Union
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertTokenizer, BertForSequenceClassification
from .base import BASIC_EMOTIONS, COMPOUND_EMOTIONS, INTENSITY_MODIFIERS
from ..tokenizer import ChineseTokenizer, EmotionTokenizer
import traceback
from ..config import MODELS_DIR

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
        # 自动初始化
        try:
            self._initialize()
        except Exception as e:
            print(f"初始化警告: {str(e)}")
        
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
                cache_dir = MODELS_DIR
                os.makedirs(cache_dir, exist_ok=True)
                
                try:
                    # 先尝试从本地加载
                    _MODEL_CACHE['tokenizer'] = AutoTokenizer.from_pretrained(
                        "IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",
                        local_files_only=True,  # 只用本地
                        cache_dir=cache_dir
                    )
                    _MODEL_CACHE['model'] = AutoModelForSequenceClassification.from_pretrained(
                        "IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",
                        local_files_only=True,
                        cache_dir=cache_dir
                    )
                    _MODEL_CACHE['is_initialized'] = True
                    print("模型从本地加载完成！")
                except Exception as e:
                    print(f"本地模型加载失败，正在尝试从网络下载: {str(e)}")
                    try:
                        # 如果本地加载失败，尝试从网络下载
                        _MODEL_CACHE['tokenizer'] = AutoTokenizer.from_pretrained(
                            "IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",
                            local_files_only=False,
                            cache_dir=cache_dir
                        )
                        _MODEL_CACHE['model'] = AutoModelForSequenceClassification.from_pretrained(
                            "IDEA-CCNL/Erlangshen-Roberta-330M-Sentiment",
                            local_files_only=False,
                            cache_dir=cache_dir
                        )
                        _MODEL_CACHE['is_initialized'] = True
                        print("模型从网络下载完成！")
                    except Exception as download_error:
                        print(f"模型下载失败: {str(download_error)}")
                        print("使用基础规则进行情感分析")
                        _MODEL_CACHE['is_initialized'] = True
            
            # 初始化分词器
            self.word_tokenizer = ChineseTokenizer()
            self._is_initialized = True
            
        except Exception as e:
            print(f"模型加载失败: {str(e)}")
            traceback.print_exc()
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
            
        try:
            if not self._is_initialized:
                self._initialize()
                
            # 如果模型仍未初始化成功，则使用规则分析
            if not _MODEL_CACHE['is_initialized'] or _MODEL_CACHE['model'] is None:
                return self._rule_based_analysis(text)
                
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
                    'keywords': emotion_keywords,
                    'emotion_scores': {
                        '正面': scores[1].item(),
                        '负面': scores[0].item()
                    }
                },
                'intensity': intensity,
                'words': words_info,
                'context': {
                    'context_type': '',
                    'keywords': [{'text': w['word']} for w in words_info] if words_info else []
                },
                'voice': {
                    'pitch': 1.0,
                    'speed': 1.0,
                    'volume': 1.0,
                    'style': ''
                }
            }
            
        except Exception as e:
            print(f"情感分析失败: {str(e)}")
            return self._rule_based_analysis(text)
    
    def _rule_based_analysis(self, text: str) -> Dict:
        """使用规则进行简单情感分析
        
        Args:
            text: 输入文本
            
        Returns:
            Dict: 情感分析结果
        """
        # 创建分词器（如果还没有）
        if self.word_tokenizer is None:
            self.word_tokenizer = ChineseTokenizer()
            
        # 使用规则进行情感分析
        positive_keywords = ['喜欢', '开心', '高兴', '快乐', '兴奋', '棒', '好', '优秀', '成功', '爱']
        negative_keywords = ['讨厌', '难过', '伤心', '悲伤', '失望', '糟糕', '差', '不好', '失败', '恨']
        
        positive_count = sum(1 for word in positive_keywords if word in text)
        negative_count = sum(1 for word in negative_keywords if word in text)
        
        # 判断情感倾向
        if positive_count > negative_count:
            emotion_label = '正面'
            confidence = min(0.6 + 0.1 * positive_count, 0.9)
            score = confidence
        elif negative_count > positive_count:
            emotion_label = '负面'
            confidence = min(0.6 + 0.1 * negative_count, 0.9)
            score = 1 - confidence
        else:
            emotion_label = '中性'
            confidence = 0.5
            score = 0.5
            
        # 分析情感强度
        intensity = self._analyze_intensity(text)
        
        # 分词
        words_info = self.word_tokenizer.tokenize(text)
            
        return {
            'text': text,
            'emotion': {
                'base_emotion': {
                    'label': emotion_label,
                    'confidence': confidence,
                    'score': score
                },
                'compound_emotions': [],
                'keywords': {},
                'emotion_scores': {
                    '正面': confidence if emotion_label == '正面' else 1 - confidence,
                    '负面': 1 - confidence if emotion_label == '正面' else confidence
                }
            },
            'intensity': intensity,
            'words': words_info,
            'context': {
                'context_type': '',
                'keywords': [{'text': w['word']} for w in words_info] if words_info else []
            },
            'voice': {
                'pitch': 1.0,
                'speed': 1.0,
                'volume': 1.0,
                'style': ''
            }
        }
    
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
                'keywords': {},
                'emotion_scores': {
                    '正面': 0.0,
                    '负面': 0.0
                }
            },
            'intensity': {
                'intensity_score': 1.0,
                'modifiers': [],
                'has_repetition': False
            },
            'words': [],
            'context': {
                'context_type': '',
                'keywords': []
            },
            'voice': {
                'pitch': 1.0,
                'speed': 1.0,
                'volume': 1.0,
                'style': ''
            }
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
            Dict[str, List[str]]: 情感关键词列表
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
        emotion_words = self.tokenizer.get_emotion_words(text)
        if not emotion_words:
            return 0.0
        intensity = 0.0
        for word, emotions in emotion_words:
            intensity += sum(emotions.values())
        return min(1.0, intensity / len(emotion_words))
    
    def analyze_keywords(self, text: str) -> List[Dict[str, Union[str, float]]]:
        """分析情感关键词
        
        Args:
            text: 输入文本
            
        Returns:
            List[Dict[str, Union[str, float]]]: 情感关键词列表
        """
        emotion_words = self.tokenizer.get_emotion_words(text)
        if not emotion_words:
            return []
        keywords = []
        for word, emotions in emotion_words:
            if emotions:
                max_emotion = max(emotions.items(), key=lambda x: x[1])
                keywords.append({
                    'word': word,
                    'emotion': max_emotion[0],
                    'score': max_emotion[1]
                })
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