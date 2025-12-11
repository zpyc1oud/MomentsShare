from datetime import datetime

from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import generics, permissions
from rest_framework.response import Response

from friends.models import Friendship
from .models import Moment
from .serializers import MomentCreateSerializer, MomentDetailSerializer, MomentListSerializer


@extend_schema(
    tags=["动态"],
    summary="发布动态",
    description="发布图文或视频动态。\n\n"
                "**图文动态 (type=IMAGE)**：最多上传9张图片，不能上传视频。\n\n"
                "**视频动态 (type=VIDEO)**：必须上传视频文件，不能上传图片。视频上传后需要异步处理。",
)
class MomentCreateView(generics.CreateAPIView):
    """发布动态接口"""
    queryset = Moment.objects.all()
    serializer_class = MomentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    tags=["动态"],
    summary="获取动态详情",
    description="根据动态ID获取详细信息，包括图片、标签等。",
)
class MomentDetailView(generics.RetrieveAPIView):
    """动态详情接口"""
    queryset = Moment.objects.all()
    serializer_class = MomentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return all moments, filtering is done in get_object
        return Moment.objects.all()

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if obj.is_deleted:
            self.permission_denied(self.request, message="内容已删除")
        if obj.type == Moment.MomentType.VIDEO and obj.video_status != Moment.VideoStatus.READY:
            if obj.author != user:
                self.permission_denied(self.request, message="视频处理中")
        return obj


@extend_schema(
    tags=["动态"],
    summary="好友动态信息流",
    description="获取已接受好友发布的动态列表，按时间倒序排列，支持分页。",
)
class FeedView(generics.ListAPIView):
    """好友动态信息流接口"""
    serializer_class = MomentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friend_ids = Friendship.objects.filter(
            Q(from_user=user, status=Friendship.Status.ACCEPTED)
            | Q(to_user=user, status=Friendship.Status.ACCEPTED)
        ).values_list("from_user_id", "to_user_id")
        ids = set()
        for pair in friend_ids:
            ids.update(pair)
        ids.discard(user.id)
        return (
            Moment.objects.filter(author_id__in=ids, is_deleted=False)
            .filter(Q(type=Moment.MomentType.IMAGE) | Q(video_status=Moment.VideoStatus.READY))
            .order_by("-created_at")
        )


@extend_schema(
    tags=["动态"],
    summary="搜索动态",
    description="根据关键词、标签、日期范围搜索动态。",
    parameters=[
        OpenApiParameter(
            name="keyword",
            type=str,
            location=OpenApiParameter.QUERY,
            description="搜索关键词（模糊匹配内容）",
            required=False,
        ),
        OpenApiParameter(
            name="label",
            type=str,
            location=OpenApiParameter.QUERY,
            description="标签名称",
            required=False,
        ),
        OpenApiParameter(
            name="start_date",
            type=str,
            location=OpenApiParameter.QUERY,
            description="开始日期 (格式: 2024-01-01)",
            required=False,
        ),
        OpenApiParameter(
            name="end_date",
            type=str,
            location=OpenApiParameter.QUERY,
            description="结束日期 (格式: 2024-01-31)",
            required=False,
        ),
    ],
)
class SearchView(generics.ListAPIView):
    """动态搜索接口"""
    serializer_class = MomentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Moment.objects.filter(is_deleted=False).filter(
            Q(type=Moment.MomentType.IMAGE) | Q(video_status=Moment.VideoStatus.READY)
        )
        keyword = self.request.query_params.get("keyword")
        label = self.request.query_params.get("label")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if keyword:
            qs = qs.filter(content__icontains=keyword)
        if label:
            qs = qs.filter(tags__name=label)
        if start_date:
            try:
                start = datetime.fromisoformat(start_date)
                qs = qs.filter(created_at__date__gte=start.date())
            except ValueError:
                pass
        if end_date:
            try:
                end = datetime.fromisoformat(end_date)
                qs = qs.filter(created_at__date__lte=end.date())
            except ValueError:
                pass
        return qs.order_by("-created_at")

