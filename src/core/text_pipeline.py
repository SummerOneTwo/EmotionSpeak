# 文本处理管道
import jieba
import spacy
from textrank4zh import TextRank4Keyword
import nltk

try:
    nlp_en = spacy.load('en_core_web_sm')
except:
    nlp_en = None
try:
    nlp_zh = spacy.load('zh_core_web_sm')
except:
    nlp_zh = None

nltk.download('punkt', quiet=True)


def process_text(text, lang='auto'):
    """分句、分词、关键词提取，支持中英文"""
    if lang == 'auto':
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            lang = 'zh'
        else:
            lang = 'en'
    if lang == 'zh':
        segs = [
            s for s in text.replace('！', '!').replace('。', '.').replace('？', '?').split('.') if s.strip()
        ]
        tr4w = TextRank4Keyword()
        tr4w.analyze(text, lower=True, window=2)
        keywords = [item.word for item in tr4w.get_keywords(10, word_min_len=1)]
    else:
        segs = nltk.sent_tokenize(text)
        if nlp_en:
            doc = nlp_en(text)
            keywords = [chunk.text for chunk in doc.noun_chunks][:10]
        else:
            keywords = []
    return segs, keywords
