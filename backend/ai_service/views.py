import base64
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, permissions
from rest_framework.response import Response

from .services import AIService
from .serializers import PolishSerializer, TagRecommendSerializer, AIResultSerializer


import logging

logger = logging.getLogger(__name__)

def _process_image(image_file):
    """Process uploaded image file to base64 string"""
    if not image_file:
        return None
    try:
        # Read file content
        image_content = image_file.read()
        logger.info(f"Processing image: size={len(image_content)} bytes, name={getattr(image_file, 'name', 'unknown')}")
        # Encode to base64
        base64_encoded = base64.b64encode(image_content).decode('utf-8')
        return base64_encoded
    except Exception as e:
        logger.error(f"Image processing failed: {e}")
        return None


@extend_schema(
    tags=["AI服务"],
    summary="文案润色与标签推荐",
    description="使用 AI 对文案进行润色优化，并同时推荐相关标签。\n\n"
                "支持文本和图片内容（多模态）。",
    request=PolishSerializer,
    responses={200: AIResultSerializer},
    examples=[
        OpenApiExample(
            "文字润色",
            value={"text": "今天天气真好"},
            request_only=True,
        ),
    ],
)
class PolishView(generics.GenericAPIView):
    """AI 文案润色接口 (MC-01)"""
    serializer_class = PolishSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = AIService()
        
        # Process image if present
        image_data = _process_image(data.get("image"))
        
        result = service.process_content(
            text=data.get("text", ""),
            image_data=image_data,
            model_name=data.get("model")
        )
        return Response(result)


@extend_schema(
    tags=["AI服务"],
    summary="标签推荐",
    description="使用 AI 根据内容推荐 3-5 个相关标签。\n\n"
                "支持文本和图片内容（多模态）。",
    request=TagRecommendSerializer,
    responses={200: {"type": "object", "properties": {"tags": {"type": "array", "items": {"type": "string"}}}}},
    examples=[
        OpenApiExample(
            "标签推荐",
            value={"text": "今天去了咖啡馆，点了一杯拿铁"},
            request_only=True,
        ),
    ],
)
class TagRecommendView(generics.GenericAPIView):
    """AI 标签推荐接口 (MC-02)"""
    serializer_class = TagRecommendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = AIService()
        
        # Process image if present
        image_data = _process_image(data.get("image"))
        
        # Reuse process_content but only return tags
        result = service.process_content(
            text=data.get("text", ""),
            image_data=image_data
        )
        
        tags = result.get("suggested_tags", [])
        return Response({"tags": tags})
