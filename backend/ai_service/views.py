from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, permissions
from rest_framework.response import Response

from .services import AIService
from .serializers import PolishSerializer, TagRecommendSerializer, AIResultSerializer


@extend_schema(
    tags=["AI服务"],
    summary="文案润色与标签推荐",
    description="使用 AI 对文案进行润色优化，并同时推荐相关标签。\n\n"
                "**注意**: 目前主要支持文本内容。",
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
        # Currently ignoring image as per implementation focus on text
        result = service.process_content(
            text=data.get("text", ""),
            model_name=data.get("model")
        )
        return Response(result)


@extend_schema(
    tags=["AI服务"],
    summary="标签推荐",
    description="使用 AI 根据内容推荐 3-5 个相关标签。\n\n"
                "**注意**: 目前主要支持文本内容。",
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
        # Reuse process_content but only return tags
        result = service.process_content(
            text=data.get("text", "")
        )
        
        tags = result.get("suggested_tags", [])
        return Response({"tags": tags})
