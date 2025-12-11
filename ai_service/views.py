from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, permissions
from rest_framework.response import Response

from .client import AIClient
from .serializers import PolishSerializer, TagRecommendSerializer


@extend_schema(
    tags=["AI服务"],
    summary="文案润色",
    description="使用 AI 对文案进行润色优化。\n\n"
                "可以提供文字、图片或两者结合。AI 会根据内容生成更加生动有趣的社交媒体文案。\n\n"
                "**注意**: text 和 image 至少提供一个。",
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

        client = AIClient()
        result = client.polish(
            text=data.get("text", ""),
            image_file=data.get("image"),
        )
        return Response({"generated_text": result})


@extend_schema(
    tags=["AI服务"],
    summary="标签推荐",
    description="使用 AI 根据内容推荐 3-5 个相关标签。\n\n"
                "可以提供文字、图片或两者结合。每个标签最多 10 个字符。\n\n"
                "**注意**: text 和 image 至少提供一个。",
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

        client = AIClient()
        tags = client.recommend_tags(
            text=data.get("text", ""),
            image_file=data.get("image"),
        )
        # Ensure constraints: 3-5 tags, each <= 10 chars
        tags = [t[:10] for t in tags][:5]
        if len(tags) < 3:
            fallback = ["推荐标签", "日常", "分享"]
            tags = tags + fallback[: 3 - len(tags)]
        return Response({"tags": tags})
