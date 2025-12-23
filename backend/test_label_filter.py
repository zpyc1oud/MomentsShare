#!/usr/bin/env python
"""
Test script for label sensitive word filtering.
"""
import os
import sys
import django

# Setup Django environment
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moments_share.settings')
django.setup()

from moments.serializers import MomentCreateSerializer
from core.dfa_filter import gfw
from rest_framework.test import APIRequestFactory

# Test 1: Check if DFA filter is loaded
print("="*60)
print("Test 1: DFA Filter Loading")
print("="*60)
print(f"DFA Filter loaded: {gfw.keyword_chains is not None}")
print(f"Keyword chains has entries: {len(gfw.keyword_chains) > 0}")

# Test 2: Check if sensitive words exist in filter
print("\n" + "="*60)
print("Test 2: Test Sensitive Word Detection")
print("="*60)

test_words = [
    ("暴力", True),
    ("色情", True),
    ("美食", False),
    ("旅行", False),
]

for word, expected_sensitive in test_words:
    is_sensitive, matched_word = gfw.exists(word)
    status = "✓" if is_sensitive == expected_sensitive else "✗"
    print(f"{status} '{word}': Sensitive={is_sensitive} (Expected={expected_sensitive})")

# Test 3: Test serializer validation with sensitive labels
print("\n" + "="*60)
print("Test 3: Serializer Validation with Sensitive Labels")
print("="*60)

factory = APIRequestFactory()
request = factory.post("/")

# Test case 1: Normal labels
print("\nTest Case 1: Normal labels")
serializer1 = MomentCreateSerializer(
    data={
        "type": "IMAGE",
        "content": "正常内容",
        "labels": ["美食", "旅行", "日常"],
    },
    context={"request": request},
)
is_valid1 = serializer1.is_valid()
print(f"  Valid: {is_valid1}")
if not is_valid1:
    print(f"  Errors: {serializer1.errors}")

# Test case 2: Single sensitive label
print("\nTest Case 2: Single sensitive label ('暴力')")
serializer2 = MomentCreateSerializer(
    data={
        "type": "IMAGE",
        "content": "正常内容",
        "labels": ["暴力", "美食"],
    },
    context={"request": request},
)
is_valid2 = serializer2.is_valid()
print(f"  Valid: {is_valid2}")
if not is_valid2:
    print(f"  Errors: {serializer2.errors}")

# Test case 3: Multiple sensitive labels
print("\nTest Case 3: Multiple sensitive labels ('暴力', '色情')")
serializer3 = MomentCreateSerializer(
    data={
        "type": "IMAGE",
        "content": "正常内容",
        "labels": ["暴力", "色情"],
    },
    context={"request": request},
)
is_valid3 = serializer3.is_valid()
print(f"  Valid: {is_valid3}")
if not is_valid3:
    print(f"  Errors: {serializer3.errors}")

# Test case 4: Mixed sensitive and normal labels
print("\nTest Case 4: Mixed sensitive and normal labels")
serializer4 = MomentCreateSerializer(
    data={
        "type": "IMAGE",
        "content": "正常内容",
        "labels": ["美食", "暴力", "旅行", "色情"],
    },
    context={"request": request},
)
is_valid4 = serializer4.is_valid()
print(f"  Valid: {is_valid4}")
if not is_valid4:
    print(f"  Errors: {serializer4.errors}")

# Test case 5: No labels
print("\nTest Case 5: No labels")
serializer5 = MomentCreateSerializer(
    data={
        "type": "IMAGE",
        "content": "正常内容",
        "labels": [],
    },
    context={"request": request},
)
is_valid5 = serializer5.is_valid()
print(f"  Valid: {is_valid5}")
if not is_valid5:
    print(f"  Errors: {serializer5.errors}")

# Summary
print("\n" + "="*60)
print("Summary")
print("="*60)
all_tests = [
    ("Normal labels", is_valid1),
    ("Single sensitive label", not is_valid2),
    ("Multiple sensitive labels", not is_valid3),
    ("Mixed labels", not is_valid4),
    ("No labels", is_valid5),
]

passed = sum(1 for _, result in all_tests if result)
total = len(all_tests)

for name, result in all_tests:
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{status} - {name}")

print(f"\nTotal: {passed}/{total} tests passed")

if passed == total:
    print("\n✓ All tests passed! Label sensitive word filtering is working correctly.")
    sys.exit(0)
else:
    print(f"\n✗ {total - passed} test(s) failed!")
    sys.exit(1)
