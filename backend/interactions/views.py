from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from rest_framework import generics, permissions

from moments.models import Moment
from .models import Comment
from .serializers import CommentSerializer


@extend_schema_view(
    get=extend_schema(
        tags=["评论"],
        summary="获取评论列表",
        description="获取指定动态的评论列表，包含嵌套回复。只返回一级评论，回复通过 replies 字段嵌套返回。",
    ),
    post=extend_schema(
        tags=["评论"],
        summary="发布评论",
        description="在指定动态下发布评论。\n\n"
                    "发布一级评论时不需要 parent_id，回复评论时需要提供 parent_id。",
        examples=[
            OpenApiExample(
                "发布一级评论",
                value={"content": "这是一条评论"},
                request_only=True,
            ),
            OpenApiExample(
                "回复评论",
                value={"content": "这是一条回复", "parent_id": 1},
                request_only=True,
            ),
        ],
    ),
)
class CommentListCreateView(generics.ListCreateAPIView):
    """评论列表和创建接口"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        moment_id = self.kwargs.get("moment_id")
        return Comment.objects.filter(moment_id=moment_id, parent__isnull=True, is_deleted=False)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        moment_id = self.kwargs.get("moment_id")
        try:
            context["moment"] = Moment.objects.get(id=moment_id, is_deleted=False)
        except Moment.DoesNotExist:
            context["moment"] = None
        return context

    def perform_create(self, serializer):
        moment = self.get_serializer_context().get("moment")
        if moment is None:
            from rest_framework.exceptions import NotFound
            raise NotFound("动态不存在或已被删除")
        serializer.save(moment=moment, author=self.request.user)

