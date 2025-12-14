from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Friendship
from .serializers import FriendshipSerializer


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
        existing = Friendship.objects.filter(from_user=request.user, to_user_id=to_user_id).first()
        if existing:
            return Response({"detail": "已发起过申请"}, status=status.HTTP_400_BAD_REQUEST)
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

