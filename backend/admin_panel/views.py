from datetime import date, timedelta

from django.db.models import Q, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from interactions.models import Comment
from moments.models import Moment
from moments.serializers import MomentListSerializer
from users.models import User
from .permissions import IsStaffUser
from .serializers import AdminTokenObtainPairSerializer


@extend_schema(
    tags=["管理后台"],
    summary="管理员登录",
    description="管理员使用手机号和密码登录，获取 JWT Token。\n\n"
                "**注意**: 只有 is_staff=True 或 is_superuser=True 的用户可以登录。",
    examples=[
        OpenApiExample(
            "登录示例",
            value={
                "phone": "13800000000",
                "password": "adminPassword123"
            },
            request_only=True,
        ),
    ],
)
class AdminLoginView(TokenObtainPairView):
    """管理员登录接口"""
    serializer_class = AdminTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    tags=["管理后台"],
    summary="内容列表",
    description="获取所有动态内容列表，包括已删除的。支持按用户过滤。",
    parameters=[
        OpenApiParameter(
            name="user_id",
            type=int,
            location=OpenApiParameter.QUERY,
            description="按用户ID过滤",
            required=False,
        ),
    ],
)
class AdminContentListView(generics.ListAPIView):
    """管理员内容列表接口"""
    serializer_class = MomentListSerializer
    permission_classes = [IsStaffUser]

    def get_queryset(self):
        qs = Moment.objects.all().order_by("-created_at")
        user_id = self.request.query_params.get("user_id")
        if user_id:
            qs = qs.filter(author_id=user_id)
        return qs


@extend_schema(
    tags=["管理后台"],
    summary="下架内容",
    description="软删除指定动态（设置 is_deleted=True），下架后用户端不可见。",
)
class AdminContentDeleteView(generics.GenericAPIView):
    """管理员下架内容接口"""
    permission_classes = [IsStaffUser]

    def delete(self, request, pk, *args, **kwargs):
        try:
            moment = Moment.objects.get(pk=pk)
        except Moment.DoesNotExist:
            return Response({"detail": "动态不存在"}, status=status.HTTP_404_NOT_FOUND)
        moment.is_deleted = True
        moment.save(update_fields=["is_deleted"])
        return Response({"detail": "已下架"})


@extend_schema(
    tags=["管理后台"],
    summary="数据统计",
    description="获取过去7天每日数据统计，包括日期、日活跃用户数、新增用户数、发帖数。",
)
class AdminStatsView(generics.GenericAPIView):
    """管理员数据统计接口"""
    permission_classes = [IsStaffUser]

    def get(self, request, *args, **kwargs):
        today = date.today()
        stats_list = []
        for i in range(7):
            current_date = today - timedelta(days=i)
            
            # Count new users for the day
            daily_new_users = User.objects.filter(created_at__date=current_date).count()
            
            # Count posts for the day
            daily_posts = Moment.objects.filter(created_at__date=current_date, is_deleted=False).count()
            
            # Calculate DAU
            dau_users = set(
                Moment.objects.filter(created_at__date=current_date).values_list("author_id", flat=True)
            ) | set(
                Comment.objects.filter(created_at__date=current_date).values_list("author_id", flat=True)
            )
            dau = len([uid for uid in dau_users if uid])
            
            stats_list.append({
                "date": current_date.isoformat(),
                "dau": dau,
                "daily_new_users": daily_new_users,
                "daily_posts": daily_posts,
            })
        
        # Sort by date ascending (optional, but often better for charts)
        stats_list.reverse()

        # 添加内容类型分布统计
        content_distribution = list(
            Moment.objects.filter(is_deleted=False)
            .values('type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # 格式化内容类型名称
        type_mapping = {
            'IMAGE': '图片动态',
            'VIDEO': '视频动态',
            'TEXT': '纯文字'
        }

        formatted_distribution = []
        for item in content_distribution:
            type_name = type_mapping.get(item['type'], item['type'])
            formatted_distribution.append({
                'type': type_name,
                'count': item['count']
            })

        # 返回包含内容分布的完整统计数据
        return Response({
            'daily_stats': stats_list,
            'content_distribution': formatted_distribution
        })
