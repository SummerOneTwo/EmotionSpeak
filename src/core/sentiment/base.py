"""情感分析基础模块"""
from typing import Dict, List

# 基本情感定义
BASIC_EMOTIONS = {
    'joy': {
        'label': '喜悦',
        'keywords': ['开心', '快乐', '高兴', '喜悦', '兴奋', '愉快', '欢乐', '欢欣', '欣喜'],
        'intensity': 1.0
    },
    'sadness': {
        'label': '悲伤',
        'keywords': ['难过', '悲伤', '痛苦', '伤心', '失落', '沮丧', '消沉', '忧郁', '哀伤'],
        'intensity': 1.0
    },
    'anger': {
        'label': '愤怒',
        'keywords': ['生气', '愤怒', '恼火', '暴怒', '不满', '气愤', '震怒', '发火', '发怒'],
        'intensity': 1.0
    },
    'fear': {
        'label': '恐惧',
        'keywords': ['害怕', '恐惧', '担心', '焦虑', '紧张', '恐慌', '畏惧', '惧怕', '惊惶'],
        'intensity': 1.0
    },
    'surprise': {
        'label': '惊讶',
        'keywords': ['惊讶', '意外', '震惊', '诧异', '惊奇', '吃惊', '愕然', '惊异', '惊诧'],
        'intensity': 1.0
    },
    'disgust': {
        'label': '厌恶',
        'keywords': ['厌恶', '反感', '嫌弃', '憎恶', '恶心', '讨厌', '厌烦', '厌弃', '厌憎'],
        'intensity': 1.0
    },
    'trust': {
        'label': '信任',
        'keywords': ['信任', '相信', '依赖', '安心', '放心', '信赖', '信服', '信从', '信靠'],
        'intensity': 1.0
    },
    'anticipation': {
        'label': '期待',
        'keywords': ['期待', '希望', '憧憬', '盼望', '期望', '企盼', '渴盼', '渴求', '向往'],
        'intensity': 1.0
    }
}

# 复合情感定义
COMPOUND_EMOTIONS = {
    'love': {
        'label': '爱',
        'components': ['joy', 'trust'],
        'keywords': ['爱', '喜欢', '热爱', '钟爱', '疼爱', '宠爱', '怜爱', '珍爱', '挚爱']
    },
    'hate': {
        'label': '恨',
        'components': ['anger', 'disgust'],
        'keywords': ['恨', '憎恨', '仇恨', '怨恨', '痛恨', '憎恶', '厌恨', '愤恨', '仇视']
    },
    'anxiety': {
        'label': '焦虑',
        'components': ['fear', 'anticipation'],
        'keywords': ['焦虑', '担忧', '忧虑', '不安', '焦躁', '烦躁', '急躁', '焦灼', '焦心']
    },
    'guilt': {
        'label': '内疚',
        'components': ['sadness', 'disgust'],
        'keywords': ['内疚', '愧疚', '自责', '悔恨', '懊悔', '悔悟', '悔过', '悔改', '悔恨']
    },
    'pride': {
        'label': '骄傲',
        'components': ['joy', 'anger'],
        'keywords': ['骄傲', '自豪', '自满', '自得', '自傲', '自大', '自负', '自恃', '自矜']
    },
    'shame': {
        'label': '羞耻',
        'components': ['sadness', 'fear'],
        'keywords': ['羞耻', '羞愧', '惭愧', '羞惭', '羞赧', '羞怯', '羞涩', '羞臊', '羞愤']
    }
}

# 情感强度修饰词
INTENSITY_MODIFIERS = {
    '非常': 1.5,
    '很': 1.3,
    '比较': 1.1,
    '有点': 0.8,
    '稍微': 0.7,
    '不太': 0.6,
    '不': 0.5
} 