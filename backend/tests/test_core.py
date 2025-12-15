"""
Tests for core module - covers all branches.
"""
import pytest
from rest_framework import status
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
class TestCustomExceptionHandler:
    """Tests for custom exception handler."""

    def test_exception_handler_with_standard_exception(self):
        """Test handler with standard DRF exception."""
        from core.exceptions import custom_exception_handler
        from rest_framework.exceptions import NotFound

        exc = NotFound("资源不存在")
        response = custom_exception_handler(exc, {})

        assert response is not None
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "detail" in response.data

    def test_exception_handler_with_validation_error(self):
        """Test handler with validation error."""
        from core.exceptions import custom_exception_handler

        exc = ValidationError({"field": ["错误信息"]})
        response = custom_exception_handler(exc, {})

        assert response is not None
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_exception_handler_with_unhandled_exception(self):
        """Test handler with unhandled exception returns 500."""
        from core.exceptions import custom_exception_handler

        exc = Exception("未处理的异常")
        response = custom_exception_handler(exc, {})

        assert response is not None
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.django_db
class TestSensitiveWords:
    """Tests for sensitive word module."""

    def test_contains_sensitive_word_with_match(self, settings):
        """Test detecting sensitive word."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = ["违禁", "敏感"]
        assert contains_sensitive_word("这是违禁内容") is True

    def test_contains_sensitive_word_no_match(self, settings):
        """Test no sensitive word detected."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = ["违禁", "敏感"]
        assert contains_sensitive_word("正常内容") is False

    def test_contains_sensitive_word_empty_text(self, settings):
        """Test with empty text."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = ["违禁"]
        assert contains_sensitive_word("") is False

    def test_contains_sensitive_word_none_text(self, settings):
        """Test with None text."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = ["违禁"]
        assert contains_sensitive_word(None) is False

    def test_contains_sensitive_word_empty_wordlist(self, settings):
        """Test with empty word list."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = []
        assert contains_sensitive_word("任何内容") is False

    def test_contains_sensitive_word_with_empty_word(self, settings):
        """Test with empty word in list."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = ["", "违禁", None]
        assert contains_sensitive_word("违禁内容") is True
        assert contains_sensitive_word("正常") is False

