from django.db.models import Avg
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiParameter
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from moments.models import Moment
from .models import Comment, Rating
from .serializers import CommentSerializer, RatingSerializer


@extend_schema_view(
    get=extend_schema(
        tags=["互动"],
        summary="获取评论列表",
        description="获取指定动态的评论列表。仅显示顶层评论，回复通过 replies 字段嵌套返回。",
    ),
    post=extend_schema(
        tags=["互动"],
        summary="发布评论",
        description="在指定动态下发布评论。\n\n"
                    "发布一级评论时不需要 parent_id，回复评论时需要提供 parent_id。",
        examples=[
            OpenApiExample(
                "发布一级评论",
                value={"content": "这是一个评论"},
                request_only=True,
            ),
            OpenApiExample(
                "回复评论",
                value={"content": "这是一个回复", "parent_id": 1},
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


@extend_schema(
    tags=["互动"],
    summary="打分/评分",
    description="对指定动态进行打星（1-5星）。如果用户已打分，则更新分数。",
    request=RatingSerializer,
    responses={201: RatingSerializer},
)
class RateView(generics.CreateAPIView):
    """打分接口"""
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # The serializer.save() method in RatingSerializer handles update_or_create
        # but we need to pass the user in context, which is already there via self.get_serializer
        rating = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["互动"],
    summary="获取平均分",
    description="获取指定动态的平均评分。",
    parameters=[
        OpenApiParameter(
            name="moment_id",
            type=int,
            location=OpenApiParameter.QUERY,
            description="动态ID",
            required=True,
        )
    ]
)
class AvgScoreView(generics.GenericAPIView):
    """获取平均分接口"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        moment_id = request.query_params.get("moment_id")
        if not moment_id:
            return Response({"detail": "Missing moment_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        avg_score = Rating.objects.filter(moment_id=moment_id).aggregate(Avg("score"))["score__avg"]
        return Response({"moment_id": int(moment_id), "avg_score": avg_score or 0.0})
