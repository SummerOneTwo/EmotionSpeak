# edge-tts TTS 封装
import os
import uuid

try:
    import edge_tts
except ImportError:
    edge_tts = None


def synthesize_speech(text, lang='zh', emotion='neutral'):
    """合成语音，返回wav文件路径"""
    out_dir = 'src/webapp/static/audio'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'{uuid.uuid4().hex}.wav')
    if edge_tts:
        voice = 'zh-CN-XiaoxiaoNeural' if lang == 'zh' else 'en-US-JennyNeural'
        rate = '+0%' if emotion == 'neutral' else ('+20%' if emotion == 'positive' else '-20%')
        try:
            import asyncio

            async def run():
                communicate = edge_tts.Communicate(text, voice, rate=rate)
                await communicate.save(out_path)

            asyncio.run(run())
            return out_path
        except Exception as e:
            print(f'edge-tts 合成失败: {e}')
    # fallback: 直接返回空音频
    with open(out_path, 'wb') as f:
        f.write(b'')
    return out_path
