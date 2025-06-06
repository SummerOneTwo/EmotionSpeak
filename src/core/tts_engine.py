"""
TTS引擎模块
"""

import os
import pyttsx3
from typing import Dict, List


class TTSEngine:
    def __init__(self, config_path="config/tts_config.json"):  # Assuming config might be used
        """初始化TTS引擎"""
        self.engine = pyttsx3.init()
        # Attempt to load voice_id from a potential config or use a default
        self.default_rate = self.engine.getProperty('rate')
        self.default_volume = self.engine.getProperty('volume')
        # Pitch is not a standard pyttsx3 property, but some engines might support it via setProperty
        self.default_pitch = 1.0  # Placeholder

    def get_available_voices(self) -> List[Dict[str, str]]:
        """获取可用的语音列表"""
        voices = self.engine.getProperty('voices')
        return [{"id": v.id, "name": v.name, "lang": v.languages} for v in voices]

    def set_voice_properties(
        self, rate: int = None, volume: float = None, pitch: float = None, voice_id: str = None
    ):
        """设置语速、音量、音高（如果支持）、可选voice_id"""
        if voice_id:
            self.engine.setProperty('voice', voice_id)

        if rate is not None:
            self.engine.setProperty('rate', rate)
        if volume is not None:
            self.engine.setProperty('volume', max(0.0, min(volume, 1.0)))
        if pitch is not None:
            # Pitch is not a standard pyttsx3 property. This is an attempt and might not work.
            # Some engines might allow setting pitch via a specific property name.
            # For example, on SAPI5, it might be possible to set it via a COM interface,
            # but pyttsx3 doesn't expose this directly in a cross-platform way.
            # We'll store it and it could be used if a specific engine driver supports it.
            try:
                # This is a speculative attempt; 'pitch' is not a standard property.
                self.engine.setProperty('pitch', pitch)
            except Exception:
                pass

    def speak_with_emotion(self, text: str, sentiment: Dict[str, float], config: Dict = None):
        """根据情感调整并朗读文本，使用配置（如果提供）"""
        polarity = sentiment.get('polarity', 0)
        classification = sentiment.get('classification', 'neutral')

        # Use provided config or defaults
        tts_config = config.get("tts", {}) if config else {}
        base_rate = tts_config.get("rate", self.default_rate)
        base_volume = tts_config.get("volume", self.default_volume)
        base_pitch = tts_config.get("pitch", self.default_pitch)  # Target pitch

        # Adjust parameters based on emotion
        # These are example adjustments, can be refined
        if classification == 'positive':
            rate_factor, volume_factor, pitch_factor = 1.1, 1.1, 1.1
        elif classification == 'negative':
            rate_factor, volume_factor, pitch_factor = 0.9, 0.9, 0.9
        else:  # neutral
            rate_factor, volume_factor, pitch_factor = 1.0, 1.0, 1.0

        adjusted_rate = int(base_rate * rate_factor)
        adjusted_volume = max(0.0, min(1.0, base_volume * volume_factor))
        adjusted_pitch = base_pitch * pitch_factor

        self.set_voice_properties(rate=adjusted_rate, volume=adjusted_volume, pitch=adjusted_pitch)

        self.engine.say(text)
        self.engine.runAndWait()

        # Reset to defaults after speaking to avoid carry-over effects
        self.set_voice_properties(
            rate=self.default_rate, volume=self.default_volume, pitch=self.default_pitch
        )

    def save_audio(self, text: str, filename: str, sentiment: Dict[str, float] = None, config: Dict = None):
        """将朗读内容保存为音频文件，可带情感"""
        if sentiment and isinstance(sentiment, dict):
            # Apply emotion-based properties before saving
            polarity = sentiment.get('polarity', 0)
            classification = sentiment.get('classification', 'neutral')

            tts_config = config.get("tts", {}) if config else {}
            base_rate = tts_config.get("rate", self.default_rate)
            base_volume = tts_config.get("volume", self.default_volume)
            base_pitch = tts_config.get("pitch", self.default_pitch)

            if classification == 'positive':
                rate_factor, volume_factor, pitch_factor = 1.1, 1.1, 1.1
            elif classification == 'negative':
                rate_factor, volume_factor, pitch_factor = 0.9, 0.9, 0.9
            else:
                rate_factor, volume_factor, pitch_factor = 1.0, 1.0, 1.0

            self.set_voice_properties(
                rate=int(base_rate * rate_factor),
                volume=max(0.0, min(1.0, base_volume * volume_factor)),
                pitch=base_pitch * pitch_factor,
            )

        # Ensure directory exists (but handle case where filename has no directory)
        dir_name = os.path.dirname(filename)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        # pyttsx3 saves to a temporary WAV first if not on NSSpeechSynthesizer (macOS)
        # Forcing .wav extension for broader compatibility if pyttsx3 doesn't handle it.
        if not filename.lower().endswith(".wav"):
            # Some engines might only support WAV.
            # To be safe, we can save as wav then convert, or just enforce wav.
            # For now, let pyttsx3 handle it, but be mindful.
            pass

        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()

        # Reset to defaults
        self.set_voice_properties(
            rate=self.default_rate, volume=self.default_volume, pitch=self.default_pitch
        )
        return filename


# Remove the standalone speak function if all functionality is within the class
# def speak(text: str, emotion: str = None):
#     """按指定情感合成语音。"""
#     # TODO: 实现
#     pass
