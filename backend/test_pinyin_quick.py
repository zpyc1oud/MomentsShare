#!/usr/bin/env python
"""
快速测试拼音匹配功能的脚本
用法: python test_pinyin_quick.py
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moments_share.settings')
django.setup()

from moments.utils import match_pinyin, get_pinyin, get_pinyin_initials, PYPINYIN_AVAILABLE

def test_cases():
    print("=" * 60)
    print("拼音搜索功能测试")
    print("=" * 60)
    print(f"pypinyin可用: {PYPINYIN_AVAILABLE}\n")
    
    if not PYPINYIN_AVAILABLE:
        print("⚠️  警告: pypinyin 未安装，拼音匹配功能不可用")
        print("   请运行: pip install pypinyin>=0.49.0\n")
    
    test_cases = [
        ("tq", "今天天气真好"),
        ("tianqi", "今天天气真好"),
        ("天气", "今天天气真好"),
        ("ms", "今天吃了美食"),
        ("meishi", "今天吃了美食"),
        ("美食", "今天吃了美食"),
        ("rj", "日常分享"),
        ("richang", "日常分享"),
        ("日常", "日常分享"),
    ]
    
    passed = 0
    failed = 0
    
    for query, text in test_cases:
        result = match_pinyin(query, text)
        status = "✓" if result else "✗"
        if result:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} 查询: '{query}' | 文本: '{text}' | 匹配: {result}")
        if PYPINYIN_AVAILABLE and result:
            print(f"   文本拼音: {get_pinyin(text)}")
            print(f"   文本首字母: {get_pinyin_initials(text)}")
        print()
    
    print("=" * 60)
    print(f"测试结果: 通过 {passed} / 失败 {failed} / 总计 {len(test_cases)}")
    print("=" * 60)

if __name__ == "__main__":
    test_cases()

