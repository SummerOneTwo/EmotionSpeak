"""
TTS引擎模块
"""

import os
import edge_tts
import asyncio
from pathlib import Path
import logging
import traceback

logger = logging.getLogger(__name__)


class EdgeTTSEngine:
    """Edge TTS引擎"""

    def __init__(self):
        """初始化TTS引擎"""
        try:
            self.voice = "zh-CN-XiaoxiaoNeural"
            self.output_dir = Path("data/audio")
            self.output_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"TTS引擎初始化完成，输出目录: {self.output_dir}")
        except Exception as e:
            logger.error(f"TTS引擎初始化失败: {str(e)}", exc_info=True)
            raise

    async def _synthesize_async(self, text: str, emotion: str = "neutral") -> str:
        """异步合成语音"""
        try:
            # 设置语音风格
            style_map = {"happy": "cheerful", "sad": "sad", "angry": "angry", "neutral": "general"}
            style = style_map.get(emotion, "general")

            # 设置语速和音调
            rate = "+0%"
            pitch = "+0Hz"
            if emotion == "happy":
                rate = "+20%"
                pitch = "+2Hz"
            elif emotion == "sad":
                rate = "-20%"
                pitch = "-2Hz"
            elif emotion == "angry":
                rate = "+30%"
                pitch = "+4Hz"

            logger.info(f"开始合成语音: text={text}, emotion={emotion}, rate={rate}, pitch={pitch}")

            # 生成输出文件名
            output_file = self.output_dir / f"{hash(text)}_{emotion}.mp3"
            logger.info(f"输出文件: {output_file}")

            # 创建通信对象
            communicate = edge_tts.Communicate(text, self.voice, rate=rate, pitch=pitch)

            # 合成语音
            await communicate.save(str(output_file))

            # 验证文件是否生成成功
            if not output_file.exists():
                raise Exception(f"语音文件生成失败: {output_file}")

            file_size = output_file.stat().st_size
            if file_size == 0:
                raise Exception(f"生成的语音文件为空: {output_file}")

            logger.info(f"语音合成完成: {output_file}, 文件大小: {file_size} 字节")
            return output_file.name  # 只返回文件名

        except Exception as e:
            logger.error(f"语音合成失败: {str(e)}", exc_info=True)
            raise Exception(f"语音合成失败: {str(e)}\n{traceback.format_exc()}")

    def synthesize(self, text: str, emotion: str = "neutral") -> str:
        """合成语音"""
        try:
            # 运行异步任务
            output_file = asyncio.run(self._synthesize_async(text, emotion))

            # 验证返回的文件名
            if not output_file:
                raise Exception("语音合成返回的文件名为空")

            # 验证文件是否存在
            full_path = self.output_dir / output_file
            if not full_path.exists():
                raise Exception(f"语音文件不存在: {full_path}")

            return output_file

        except Exception as e:
            logger.error(f"语音合成失败: {str(e)}", exc_info=True)
            raise Exception(f"语音合成失败: {str(e)}\n{traceback.format_exc()}")
