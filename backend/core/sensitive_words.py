from typing import Optional

from django.conf import settings


def contains_sensitive_word(text: Optional[str]) -> bool:
    """
    Simple sensitive word check.
    Returns True if text contains any configured sensitive word.
    """
    if not text:
        return False
    words = getattr(settings, "SENSITIVE_WORDS", [])
    for word in words:
        # Skip empty or None words in the list
        if word and word in text:
            return True
    return False

