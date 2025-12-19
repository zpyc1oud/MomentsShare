from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Case, When, Value, IntegerField

from .models import Friendship
from .serializers import FriendshipSerializer
from users.models import User
from users.serializers import UserSerializer


@extend_schema(
    tags=["好友"],
    summary="发起好友申请",
    description="向指定用户发起好友申请。",
    examples=[
        OpenApiExample(
            "申请示例",
            value={"to_user_id": 2},
            request_only=True,
        ),
    ],
)
class FriendRequestView(generics.GenericAPIView):
    """发起好友申请接口"""
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get("to_user_id")
        if not to_user_id:
            return Response({"detail": "缺少 to_user_id"}, status=status.HTTP_400_BAD_REQUEST)
        if int(to_user_id) == request.user.id:
            return Response({"detail": "不能向自己发起申请"}, status=status.HTTP_400_BAD_REQUEST)

        # 检查是否已存在关系
        existing = Friendship.objects.filter(from_user=request.user, to_user_id=to_user_id).first()
        if existing:
            if existing.status == Friendship.Status.PENDING:
                return Response({"detail": "已发起过申请"}, status=status.HTTP_400_BAD_REQUEST)
            elif existing.status == Friendship.Status.ACCEPTED:
                return Response({"detail": "已经是好友"}, status=status.HTTP_400_BAD_REQUEST)
            elif existing.status == Friendship.Status.REJECTED:
                # 重新申请，将状态改为PENDING
                existing.status = Friendship.Status.PENDING
                existing.save(update_fields=["status", "updated_at"])
                return Response(FriendshipSerializer(existing).data, status=status.HTTP_200_OK)

        # 创建新的好友申请
        friendship = Friendship.objects.create(from_user=request.user, to_user_id=to_user_id, status=Friendship.Status.PENDING)
        return Response(FriendshipSerializer(friendship).data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["好友"],
    summary="响应好友申请",
    description="接受或拒绝收到的好友申请。\n\n"
                "**action**: `accept` 接受 或 `reject` 拒绝",
    examples=[
        OpenApiExample(
            "接受申请",
            value={"request_id": 1, "action": "accept"},
            request_only=True,
        ),
        OpenApiExample(
            "拒绝申请",
            value={"request_id": 1, "action": "reject"},
            request_only=True,
        ),
    ],
)
class FriendRespondView(generics.GenericAPIView):
    """响应好友申请接口"""
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get("request_id")
        action = request.data.get("action")
        if not request_id or action not in ["accept", "reject"]:
            return Response({"detail": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            friendship = Friendship.objects.get(id=request_id)
        except Friendship.DoesNotExist:
            return Response({"detail": "申请不存在"}, status=status.HTTP_404_NOT_FOUND)
        if friendship.to_user != request.user:
            return Response({"detail": "无权处理该申请"}, status=status.HTTP_403_FORBIDDEN)
        if action == "accept":
            friendship.status = Friendship.Status.ACCEPTED
        else:
            friendship.status = Friendship.Status.REJECTED
        friendship.save(update_fields=["status", "updated_at"])
        return Response(FriendshipSerializer(friendship).data)


@extend_schema(
    tags=["好友"],
    summary="删除好友",
    description="删除与指定用户的好友关系。",
)
@extend_schema(
    tags=["好友"],
    summary="获取好友列表",
    description="获取当前用户的好友列表，包含已接受的好友。",
)
class FriendListView(generics.ListAPIView):
    """获取好友列表接口"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        # 获取已接受的好友关系
        friendships = Friendship.objects.filter(
            Q(from_user=user) | Q(to_user=user),
            status=Friendship.Status.ACCEPTED
        ).select_related('from_user', 'to_user')

        # 提取好友用户ID
        friend_ids = []
        for friendship in friendships:
            if friendship.from_user == user:
                friend_ids.append(friendship.to_user_id)
            else:
                friend_ids.append(friendship.from_user_id)

        # 按好友创建时间排序
        case_conditions = []
        for i, friendship in enumerate(friendships):
            if friendship.from_user == user:
                case_conditions.append(
                    When(id=friendship.to_user_id, then=Value(i))
                )
            else:
                case_conditions.append(
                    When(id=friendship.from_user_id, then=Value(i))
                )

        return User.objects.filter(id__in=friend_ids).annotate(
            friendship_order=Case(*case_conditions, default=Value(999), output_field=IntegerField())
        ).order_by('friendship_order')


@extend_schema(
    tags=["好友"],
    summary="搜索用户",
    description="搜索用户，用于添加好友。支持按昵称或手机号搜索。",
    examples=[
        OpenApiExample(
            "搜索用户",
            value={"keyword": "张三"},
            request_only=True,
        ),
    ],
)
@extend_schema(
    tags=["好友"],
    summary="获取待处理好友申请",
    description="获取当前用户收到的待处理好友申请。",
)
class PendingRequestsView(generics.ListAPIView):
    """获取待处理好友申请接口"""
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(
            to_user=user,
            status=Friendship.Status.PENDING
        ).select_related('from_user').order_by('-created_at')


class UserSearchView(generics.ListAPIView):
    """搜索用户接口"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', '').strip()
        user = self.request.user

        if not keyword:
            return User.objects.none()

        # 搜索用户，只排除自己，允许搜索所有其他用户（包括已有好友关系的用户）
        return User.objects.filter(
            Q(nickname__icontains=keyword) | Q(phone__icontains=keyword),
            is_active=True
        ).exclude(
            id=user.id
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class FriendDeleteView(generics.DestroyAPIView):
    """删除好友接口"""
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "user_id"

    def get_object(self):
        user = self.request.user
        other_id = self.kwargs.get(self.lookup_url_kwarg)
        friendship = Friendship.objects.filter(
            from_user=user, to_user_id=other_id
        ).first() or Friendship.objects.filter(from_user_id=other_id, to_user=user).first()
        if not friendship:
            self.permission_denied(self.request, message="未找到好友关系")
        return friendship

