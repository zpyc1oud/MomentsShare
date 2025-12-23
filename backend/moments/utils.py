"""
拼音匹配工具函数
"""
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

# 延迟导入pypinyin，避免未安装时影响其他功能
try:
    from pypinyin import lazy_pinyin, Style
    PYPINYIN_AVAILABLE = True
    logger.info("pypinyin module loaded successfully")
except ImportError:
    PYPINYIN_AVAILABLE = False
    logger.warning("pypinyin module not available. Install it with: pip install pypinyin")
    # 提供占位函数，避免导入错误
    def lazy_pinyin(text, style=None):
        return []
    Style = type('Style', (), {'NORMAL': None, 'FIRST_LETTER': None})()


def get_pinyin(text: str) -> str:
    """
    获取文本的拼音（全拼）
    例如: "天气" -> "tianqi"
    """
    if not text or not PYPINYIN_AVAILABLE:
        return ""
    return "".join(lazy_pinyin(text, style=Style.NORMAL))


def get_pinyin_initials(text: str) -> str:
    """
    获取文本的拼音首字母
    例如: "天气" -> "tq"
    """
    if not text or not PYPINYIN_AVAILABLE:
        return ""
    return "".join(lazy_pinyin(text, style=Style.FIRST_LETTER))


def match_pinyin(query: str, text: str) -> bool:
    """
    检查查询词是否匹配文本（支持中文、全拼、首字母）
    
    Args:
        query: 用户输入的查询词（可能是中文、拼音或首字母）
        text: 要匹配的文本
    
    Returns:
        bool: 是否匹配
    """
    if not query or not text:
        return False
    
    # 如果pypinyin不可用，只进行直接匹配
    if not PYPINYIN_AVAILABLE:
        return query.lower().strip() in text.lower().strip()
    
    query_lower = query.lower().strip()
    text_lower = text.lower().strip()
    
    # 1. 直接包含匹配（中文或英文）
    if query_lower in text_lower:
        return True
    
    # 2. 拼音全拼匹配（连续匹配）
    try:
        text_pinyin = get_pinyin(text).lower()
        if text_pinyin and query_lower in text_pinyin:
            return True
        
        # 3. 拼音首字母匹配（连续匹配）
        text_initials = get_pinyin_initials(text).lower()
        if text_initials and query_lower in text_initials:
            return True
        
        # 4. 如果查询词包含中文，转换为拼音后匹配
        if any('\u4e00' <= char <= '\u9fff' for char in query):
            query_pinyin = get_pinyin(query).lower()
            if query_pinyin:
                if query_pinyin in text_pinyin:
                    return True
                # 也检查首字母
                query_initials = get_pinyin_initials(query).lower()
                if query_initials and query_initials in text_initials:
                    return True
        
        # 5. 分词匹配：检查文本中每个词的拼音
        # 将文本按常见分隔符分割
        import re
        # 分割中文字符和标点符号
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', text)
        
        for word in words:
            if not word:
                continue
            
            # 检查词的拼音全拼
            word_pinyin = get_pinyin(word).lower()
            if word_pinyin and query_lower in word_pinyin:
                return True
            
            # 检查词的拼音首字母
            word_initials = get_pinyin_initials(word).lower()
            if word_initials and query_lower in word_initials:
                return True
            
            # 如果查询词较短，检查是否匹配词的开头部分
            if len(query_lower) <= len(word_pinyin):
                if word_pinyin.startswith(query_lower) or word_initials.startswith(query_lower):
                    return True
        
        # 6. 滑动窗口匹配：检查文本中任意连续字符的拼音组合
        # 这对于匹配部分拼音很有用，例如 "tian" 匹配 "今天天气真好" 中的 "天"
        if len(query_lower) <= 10 and len(text) <= 100:  # 限制长度以提高性能
            for i in range(len(text)):
                # 尝试不同长度的窗口
                for window_len in range(1, min(len(query_lower) + 3, len(text) - i + 1)):
                    segment = text[i:i + window_len]
                    if not segment:
                        continue
                    
                    segment_pinyin = get_pinyin(segment).lower()
                    segment_initials = get_pinyin_initials(segment).lower()
                    
                    # 检查是否匹配
                    if segment_pinyin and query_lower in segment_pinyin:
                        return True
                    if segment_initials and query_lower in segment_initials:
                        return True
                    
                    # 检查是否以查询词开头
                    if segment_pinyin.startswith(query_lower) or segment_initials.startswith(query_lower):
                        return True
    except Exception:
        # 如果拼音处理出错，回退到直接匹配
        pass
    
    return False


def build_pinyin_q(query: str) -> List:
    """
    构建支持拼音匹配的Django Q对象列表
    
    Args:
        query: 用户输入的查询词
    
    Returns:
        List[Q]: Q对象列表，用于Django ORM查询
    """
    from django.db.models import Q
    
    if not query:
        return []
    
    query_lower = query.lower().strip()
    q_list = []
    
    # 1. 直接包含匹配
    q_list.append(Q(content__icontains=query))
    
    # 2. 如果查询词看起来像拼音（只包含字母），尝试拼音匹配
    if query.isalpha():
        # 这里我们需要在Python层面进行过滤，因为Django ORM不支持拼音匹配
        # 所以先获取所有可能匹配的记录，然后在Python中过滤
        # 为了性能，我们仍然先用content__icontains做初步筛选
        pass
    
    return q_list

