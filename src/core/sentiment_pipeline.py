# 情感分析管道
from snownlp import SnowNLP
from textblob import TextBlob
from transformers import pipeline
import nltk

try:
    sentiment_en = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
except:
    sentiment_en = None

nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()


def analyze_sentiment_batch(segs, lang='auto'):
    results = []
    for s in segs:
        if lang == 'auto':
            if any('\u4e00' <= c <= '\u9fff' for c in s):
                lang = 'zh'
            else:
                lang = 'en'
        if lang == 'zh':
            snlp = SnowNLP(s)
            polarity = snlp.sentiments * 2 - 1
            classification = 'positive' if polarity > 0.1 else 'negative' if polarity < -0.1 else 'neutral'
            results.append({'polarity': polarity, 'classification': classification})
        else:
            if sentiment_en:
                label = sentiment_en(s)[0]
                polarity = label['score'] if label['label'] == 'POSITIVE' else -label['score']
                classification = (
                    'positive' if polarity > 0.1 else 'negative' if polarity < -0.1 else 'neutral'
                )
            else:
                tb = TextBlob(s)
                polarity = tb.sentiment.polarity
                classification = (
                    'positive' if polarity > 0.1 else 'negative' if polarity < -0.1 else 'neutral'
                )
            results.append({'polarity': polarity, 'classification': classification})
    return results
