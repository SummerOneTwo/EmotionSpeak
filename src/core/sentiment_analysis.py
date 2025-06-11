"""
情感分析核心模块
"""

import os
import logging
import numpy as np
from typing import Dict, List, Union, Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from snownlp import SnowNLP
from textblob import TextBlob
import jieba
import jieba.posseg as pseg

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """情感分析器类"""

    def __init__(self, model_path: Optional[str] = None):
        """
        初始化情感分析器

        Args:
            model_path: 预训练模型路径，如果为None则使用默认模型
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"使用设备: {self.device}")

        # 初始化模型
        self._init_models(model_path)

        # 情感词典
        self.emotion_dict = self._load_emotion_dict()

    def _init_models(self, model_path: Optional[str]):
        """初始化所有模型"""
        try:
            # BERT模型
            model_name = model_path or "bert-base-chinese"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.to(self.device)

            # 加载其他模型
            self.snownlp = SnowNLP
            self.textblob = TextBlob

            logger.info("模型初始化成功")
        except Exception as e:
            logger.error(f"模型初始化失败: {str(e)}")
            raise

    def _load_emotion_dict(self) -> Dict:
        """加载情感词典"""
        # TODO: 实现情感词典加载
        return {}

    def analyze(self, text: str) -> Dict:
        """
        基础情感分析

        Args:
            text: 输入文本

        Returns:
            包含情感分析结果的字典
        """
        try:
            # BERT分析
            bert_result = self._bert_analyze(text)

            # SnowNLP分析
            snownlp_result = self._snownlp_analyze(text)

            # TextBlob分析
            textblob_result = self._textblob_analyze(text)

            # 融合结果
            result = self._merge_results(bert_result, snownlp_result, textblob_result)

            return result
        except Exception as e:
            logger.error(f"情感分析失败: {str(e)}")
            raise

    def analyze_detailed(self, text: str) -> Dict:
        """
        详细情感分析

        Args:
            text: 输入文本

        Returns:
            包含详细情感分析结果的字典
        """
        try:
            # 基础分析
            base_result = self.analyze(text)

            # 情感词分析
            emotion_words = self._analyze_emotion_words(text)

            # 情感转折分析
            transitions = self._analyze_transitions(text)

            # 情感强度分析
            intensity = self._analyze_intensity(text)

            # 合并结果
            detailed_result = {
                **base_result,
                'emotion_words': emotion_words,
                'transitions': transitions,
                'intensity': intensity,
            }

            return detailed_result
        except Exception as e:
            logger.error(f"详细情感分析失败: {str(e)}")
            raise

    def _bert_analyze(self, text: str) -> Dict:
        """使用BERT模型进行分析"""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.softmax(outputs.logits, dim=1)

        return {
            'polarity': 'positive' if scores[0][1] > scores[0][0] else 'negative',
            'confidence': float(scores[0].max()),
            'scores': scores[0].tolist(),
        }

    def _snownlp_analyze(self, text: str) -> Dict:
        """使用SnowNLP进行分析"""
        s = self.snownlp(text)
        return {
            'polarity': 'positive' if s.sentiments > 0.5 else 'negative',
            'confidence': abs(s.sentiments - 0.5) * 2,
            'score': s.sentiments,
        }

    def _textblob_analyze(self, text: str) -> Dict:
        """使用TextBlob进行分析"""
        blob = self.textblob(text)
        return {
            'polarity': 'positive' if blob.sentiment.polarity > 0 else 'negative',
            'confidence': abs(blob.sentiment.polarity),
            'score': blob.sentiment.polarity,
        }

    def _merge_results(self, *results) -> Dict:
        """合并多个分析结果"""
        # 加权平均
        weights = {'bert': 0.5, 'snownlp': 0.3, 'textblob': 0.2}
        final_score = 0
        total_weight = 0

        for result, weight in zip(results, weights.values()):
            score = result['score'] if 'score' in result else result['scores'][1]
            final_score += score * weight
            total_weight += weight

        final_score /= total_weight

        return {
            'polarity': 'positive' if final_score > 0.5 else 'negative',
            'confidence': abs(final_score - 0.5) * 2,
            'score': final_score,
        }

    def _analyze_emotion_words(self, text: str) -> List[Dict]:
        """分析文本中的情感词"""
        words = pseg.cut(text)
        emotion_words = []

        for word, flag in words:
            if word in self.emotion_dict:
                emotion_words.append(
                    {'word': word, 'emotion': self.emotion_dict[word], 'position': text.find(word)}
                )

        return emotion_words

    def _analyze_transitions(self, text: str) -> List[Dict]:
        """分析情感转折"""
        # TODO: 实现情感转折分析
        return []

    def _analyze_intensity(self, text: str) -> float:
        """分析情感强度"""
        # TODO: 实现情感强度分析
        return 0.5
