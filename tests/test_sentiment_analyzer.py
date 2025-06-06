import sys, os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from core.sentiment_analyzer import analyze_sentiment, classify_emotion, batch_analyze


def test_analyze_sentiment_en():
    res = analyze_sentiment("I love this product! It's amazing.")
    assert isinstance(res, dict)
    assert res['polarity'] > 0


def test_analyze_sentiment_cn():
    res = analyze_sentiment("我讨厌这个服务。")
    assert isinstance(res, dict)
    assert res['polarity'] < 0


def test_classify_emotion():
    assert classify_emotion(0.5) == 'positive'
    assert classify_emotion(-0.5) == 'negative'
    assert classify_emotion(0.0) == 'neutral'


def test_batch_analyze():
    sentences = ["Good job.", "坏透了。", "It's ok."]
    results = batch_analyze(sentences)
    assert isinstance(results, list)
    assert len(results) == 3
    # 检查每项都有classification
    for r in results:
        assert 'polarity' in r and 'classification' in r
