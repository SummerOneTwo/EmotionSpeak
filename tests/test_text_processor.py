import sys, os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from core.text_processor import TextProcessor


def test_clean_text():
    tp = TextProcessor()
    text = " Hello,  世界!! $$$   "
    assert tp.clean_text(text) == "Hello 世界 !!"


def test_split_sentences():
    tp = TextProcessor()
    text = "Hello world! 你好世界。How are you?今天天气不错！"
    segs = tp.split_sentences(text)
    assert any("Hello world" in s for s in segs)
    assert any("你好世界" in s for s in segs)
    assert any("How are you" in s for s in segs)
    assert any("今天天气不错" in s for s in segs)


def test_detect_punctuation():
    tp = TextProcessor()
    sent = "Wow!!! Really? Hmm..."
    d = tp.detect_punctuation(sent)
    assert d['exclamations'] == 3
    assert d['questions'] == 1
    assert d['ellipses'] == 1


def test_extract_keywords_en():
    tp = TextProcessor()
    text = "This is a test sentence for keyword extraction."
    kws = tp.extract_keywords(text)
    assert isinstance(kws, list)
    # 至少包含test或sentence
    assert any(w in ['test', 'sentence'] for w in kws)


def test_extract_keywords_cn():
    tp = TextProcessor()
    text = "今天天气真好，适合出去散步。"
    kws = tp.extract_keywords(text)
    # 只要包含“天气”两个字即可
    assert any("天气" in w for w in kws)
