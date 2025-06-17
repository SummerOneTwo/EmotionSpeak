"""
高级语音合成引擎模块
支持基于情感分析结果的智能语音参数调整
"""

import os
import edge_tts
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
from .sentiment_analysis import analyze_text_for_tts
from .sentiment.analyzer import SentimentAnalyzer
from .sentiment.base import BASIC_EMOTIONS, COMPOUND_EMOTIONS


class TTSEngine:
    """Text-to-Speech engine using Microsoft Edge TTS"""
    
    voice_map = {
        '晓晓': 'zh-CN-XiaoxiaoNeural',
        '云野': 'zh-CN-YunyeNeural',
        '晓伊': 'zh-CN-XiaoyiNeural',
        '云希': 'zh-CN-YunxiNeural',
        '晓墨': 'zh-CN-XiaomoNeural',
        '云泽': 'zh-CN-YunzeNeural'
    }
    
    def __init__(self):
        """Initialize TTS engine"""
        self.output_dir = 'data/audio'
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def _synthesize_async(self, text: str, voice: str, output_file: str):
        """Synthesize speech asynchronously"""
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
    
    def synthesize(self, text: str, voice: str = '晓晓', output_file: str = None) -> str:
        """Synthesize speech from text"""
        if output_file is None:
            output_file = os.path.join(self.output_dir, f'speech_{hash(text)}.mp3')
        
        asyncio.run(self._synthesize_async(text, self.voice_map.get(voice, 'zh-CN-XiaoxiaoNeural'), output_file))
        return output_file
    
    def get_available_voices(self) -> dict:
        """Get available voice mappings"""
        return self.voice_map

    def synthesize_with_emotion(self, text: str, auto_analyze: bool = True, output_file: str = None) -> str:
        """根据情感分析结果自适应参数合成语音"""
        try:
            if auto_analyze:
                analyzer = SentimentAnalyzer()
                result = analyzer.analyze(text)
                base_emotion = result['emotion']['base_emotion']['label']
                intensity = result['intensity']['intensity_score']
                compound_emotions = result['emotion'].get('compound_emotions', [])
            else:
                base_emotion = '中性'
                intensity = 1.0
                compound_emotions = []

            # 参数映射
            param_map = {
                '喜悦':  {'voice': '晓晓', 'pitch': 1.2, 'rate': 1.1, 'style': 'cheerful'},
                '悲伤':  {'voice': '云希', 'pitch': 0.9, 'rate': 0.9, 'style': 'sad'},
                '愤怒':  {'voice': '云泽', 'pitch': 1.3, 'rate': 1.2, 'style': 'angry'},
                '恐惧':  {'voice': '晓伊', 'pitch': 1.1, 'rate': 1.0, 'style': 'fearful'},
                '惊讶':  {'voice': '晓晓', 'pitch': 1.2, 'rate': 1.2, 'style': 'excited'},
                '厌恶':  {'voice': '云希', 'pitch': 0.8, 'rate': 0.9, 'style': 'disgusted'},
                '信任':  {'voice': '云野', 'pitch': 1.0, 'rate': 1.0, 'style': 'calm'},
                '期待':  {'voice': '晓伊', 'pitch': 1.1, 'rate': 1.1, 'style': 'hopeful'},
                '中性':  {'voice': '晓晓', 'pitch': 1.0, 'rate': 1.0, 'style': 'general'}
            }
            # 复合情感优先
            if compound_emotions:
                comp = compound_emotions[0]['label']
                if comp == '爱':
                    param = {'voice': '云野', 'pitch': 1.1, 'rate': 1.05, 'style': 'affectionate'}
                elif comp == '恨':
                    param = {'voice': '云泽', 'pitch': 1.3, 'rate': 1.2, 'style': 'angry'}
                elif comp == '焦虑':
                    param = {'voice': '晓伊', 'pitch': 1.0, 'rate': 1.15, 'style': 'anxious'}
                elif comp == '内疚':
                    param = {'voice': '云希', 'pitch': 0.8, 'rate': 0.9, 'style': 'sad'}
                elif comp == '骄傲':
                    param = {'voice': '晓晓', 'pitch': 1.2, 'rate': 1.1, 'style': 'proud'}
                elif comp == '羞耻':
                    param = {'voice': '晓伊', 'pitch': 0.9, 'rate': 0.95, 'style': 'shy'}
                else:
                    param = param_map.get(base_emotion, param_map['中性'])
            else:
                param = param_map.get(base_emotion, param_map['中性'])
            # 根据强度微调
            param['pitch'] *= intensity
            param['rate'] *= intensity
            voice = self.voice_map.get(param['voice'], 'zh-CN-XiaoxiaoNeural')
            pitch = param['pitch']
            rate = param['rate']
            style = param['style']
            if output_file is None:
                output_file = os.path.join(self.output_dir, f'speech_{hash(text)}.mp3')
            try:
                asyncio.run(self._synthesize_async_with_params(text, voice, output_file, pitch, rate, style))
            except Exception as e:
                raise RuntimeError(f"TTS合成失败: {str(e)}")
            # 合成后自动删除音频文件
            try:
                if os.path.exists(output_file):
                    os.remove(output_file)
            except Exception:
                pass
            return output_file
        except Exception as e:
            raise

    async def _synthesize_async_with_params(self, text: str, voice: str, output_file: str, pitch: float, rate: float, style: str):
        """支持参数自适应的异步合成"""
        communicate = edge_tts.Communicate(text, voice, rate=f"{rate}", pitch=f"{pitch}", style=style)
        await communicate.save(output_file)

# 为了兼容性，保留别名
AdvancedTTSEngine = TTSEngine
