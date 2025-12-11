"""
AI Client using Google Generative AI (Gemini) for polish and tag recommendation.
"""
import base64
import json
import logging
import re
from typing import List, Optional

from django.conf import settings

logger = logging.getLogger(__name__)


def _get_genai_model():
    """Lazy import and instantiate Google Generative AI model."""
    try:
        import google.generativeai as genai
    except ImportError:
        logger.error("google-generativeai package not installed. Run: pip install google-generativeai")
        return None

    api_key = getattr(settings, "GOOGLE_API_KEY", None)
    if not api_key:
        logger.warning("GOOGLE_API_KEY not configured, AI features will use fallback.")
        return None

    genai.configure(api_key=api_key)
    model_name = getattr(settings, "GOOGLE_AI_MODEL", "gemini-1.5-flash")
    return genai.GenerativeModel(model_name)


class AIClient:
    """Google Generative AI based client for content polish and tag recommendation."""

    def __init__(self):
        self.model = _get_genai_model()

    def _encode_image_to_base64(self, image_file) -> Optional[str]:
        """Encode uploaded image file to base64."""
        try:
            image_file.seek(0)
            data = image_file.read()
            return base64.standard_b64encode(data).decode("utf-8")
        except Exception as exc:
            logger.warning("Failed to encode image: %s", exc)
            return None

    def _get_image_mime_type(self, image_file) -> str:
        """Detect image MIME type from file content or name."""
        try:
            name = getattr(image_file, "name", "") or ""
            name_lower = name.lower()
            if name_lower.endswith(".png"):
                return "image/png"
            elif name_lower.endswith(".gif"):
                return "image/gif"
            elif name_lower.endswith(".webp"):
                return "image/webp"
            return "image/jpeg"
        except Exception:
            return "image/jpeg"

    def _generate(self, prompt: str, image_file=None, max_tokens: int = 512) -> Optional[str]:
        """Send generation request to Gemini."""
        if not self.model:
            return None
        try:
            contents = []
            if image_file:
                b64 = self._encode_image_to_base64(image_file)
                if b64:
                    mime_type = self._get_image_mime_type(image_file)
                    contents.append({
                        "mime_type": mime_type,
                        "data": b64,
                    })
            contents.append(prompt)

            response = self.model.generate_content(
                contents,
                generation_config={
                    "max_output_tokens": max_tokens,
                    "temperature": 0.7,
                },
            )
            if response and response.text:
                return response.text.strip()
            return None
        except Exception as exc:
            logger.exception("Google AI API error: %s", exc)
            return None

    def polish(self, text: str = "", image_file=None) -> str:
        """
        Polish user text using AI, optionally considering image content.
        Returns polished text or fallback if AI unavailable.
        """
        if image_file:
            if text:
                prompt = (
                    f"你是一个社交媒体文案助手。用户提供了一张图片和一段简短的文字：\n\n"
                    f"原文：{text}\n\n"
                    f"请根据图片内容和原文，润色并生成一段更加生动、有趣、适合社交媒体分享的文案。"
                    f"直接返回润色后的文案，不要添加额外说明。"
                )
            else:
                prompt = (
                    "你是一个社交媒体文案助手。请根据这张图片的内容，"
                    "生成一段生动、有趣、适合社交媒体分享的文案。"
                    "直接返回文案，不要添加额外说明。"
                )
        else:
            prompt = (
                f"你是一个社交媒体文案助手。用户提供了一段简短的文字：\n\n"
                f"原文：{text}\n\n"
                f"请润色这段文字，使其更加生动、有趣、适合社交媒体分享。"
                f"直接返回润色后的文案，不要添加额外说明。"
            )

        result = self._generate(prompt, image_file)
        if result:
            return result

        # Fallback
        base = text or "精彩瞬间"
        return f"✨ {base} ✨"

    def recommend_tags(self, text: str = "", image_file=None) -> List[str]:
        """
        Recommend 3-5 tags based on text and/or image.
        Each tag is at most 10 characters.
        """
        if image_file:
            if text:
                prompt = (
                    f"你是一个标签推荐助手。根据用户提供的图片和文字内容：\n\n"
                    f"内容：{text}\n\n"
                    f"推荐3到5个适合社交媒体的标签。"
                    f"每个标签不超过10个字符，不要带#号。"
                    f"以JSON数组格式返回，例如：[\"标签1\", \"标签2\", \"标签3\"]"
                )
            else:
                prompt = (
                    "你是一个标签推荐助手。请根据这张图片的内容，"
                    "推荐3到5个适合社交媒体的标签。"
                    "每个标签不超过10个字符，不要带#号。"
                    "以JSON数组格式返回，例如：[\"标签1\", \"标签2\", \"标签3\"]"
                )
        else:
            prompt = (
                f"你是一个标签推荐助手。根据用户提供的文字内容：\n\n"
                f"内容：{text}\n\n"
                f"推荐3到5个适合社交媒体的标签。"
                f"每个标签不超过10个字符，不要带#号。"
                f"以JSON数组格式返回，例如：[\"标签1\", \"标签2\", \"标签3\"]"
            )

        result = self._generate(prompt, image_file, max_tokens=128)
        if result:
            tags = self._parse_tags(result)
            if tags:
                return tags

        # Fallback
        return ["日常", "分享", "生活"]

    def _parse_tags(self, raw: str) -> List[str]:
        """Parse JSON array of tags from model response."""
        # Try to extract JSON array from response
        match = re.search(r'\[.*?\]', raw, re.DOTALL)
        if match:
            try:
                tags = json.loads(match.group())
                if isinstance(tags, list):
                    # Ensure each tag is string and at most 10 chars
                    return [str(t)[:10] for t in tags if t][:5]
            except json.JSONDecodeError:
                pass

        # Fallback: split by comma or Chinese comma
        parts = re.split(r'[,，、\s]+', raw)
        tags = [p.strip().strip('"\'#').strip() for p in parts if p.strip()]
        return [t[:10] for t in tags if t][:5]
