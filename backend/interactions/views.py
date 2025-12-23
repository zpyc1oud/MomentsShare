from django.db.models import Avg, Q, Max, Count
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiParameter
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from moments.models import Moment
from users.models import User
from .models import Comment, Rating, Like, Message
from .serializers import CommentSerializer, RatingSerializer, LikeSerializer, MessageSerializer, ConversationSerializer


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


@extend_schema(
    tags=["互动"],
    summary="点赞/取消点赞",
    description="对指定动态进行点赞或取消点赞操作。如果用户未点赞则点赞，已点赞则取消点赞。",
    request=LikeSerializer,
    responses={201: LikeSerializer, 200: {"detail": "取消点赞成功"}},
)
class LikeView(generics.CreateAPIView):
    """点赞接口"""
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        moment_id = kwargs.get("moment_id")
        try:
            moment = Moment.objects.get(id=moment_id, is_deleted=False)
        except Moment.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound("动态不存在或已被删除")

        # 检查是否已经点赞
        like_instance = Like.objects.filter(moment=moment, user=request.user).first()

        if like_instance:
            # 取消点赞
            like_instance.delete()
            return Response({
                "detail": "取消点赞成功",
                "liked": False,
                "likes_count": Like.objects.filter(moment=moment).count()
            }, status=status.HTTP_200_OK)
        else:
            # 点赞
            like = Like.objects.create(moment=moment, user=request.user)
            serializer = self.get_serializer(like)
            return Response({
                "detail": "点赞成功",
                "liked": True,
                "likes_count": Like.objects.filter(moment=moment).count(),
                "like": serializer.data
            }, status=status.HTTP_201_CREATED)


# ========== 私信相关视图 ==========

@extend_schema(
    tags=["私信"],
    summary="发送私信",
    description="向好友发送私信消息。只能给已添加的好友发送私信。",
    request=MessageSerializer,
    responses={201: MessageSerializer},
)
class SendMessageView(generics.CreateAPIView):
    """发送私信接口"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(
    tags=["私信"],
    summary="获取会话列表",
    description="获取当前用户的所有私信会话列表，按最后消息时间倒序排列。",
)
class ConversationListView(generics.GenericAPIView):
    """会话列表接口"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        
        # 获取所有与当前用户相关的消息
        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))
        
        # 找出所有对话的用户
        conversation_users = set()
        for msg in messages:
            if msg.sender_id == user.id:
                conversation_users.add(msg.receiver_id)
            else:
                conversation_users.add(msg.sender_id)
        
        conversations = []
        for other_user_id in conversation_users:
            other_user = User.objects.get(id=other_user_id)
            
            # 获取与该用户的最后一条消息
            last_msg = Message.objects.filter(
                (Q(sender=user) & Q(receiver_id=other_user_id)) |
                (Q(sender_id=other_user_id) & Q(receiver=user))
            ).order_by('-created_at').first()
            
            # 获取未读消息数
            unread_count = Message.objects.filter(
                sender_id=other_user_id,
                receiver=user,
                is_read=False
            ).count()
            
            conversations.append({
                'user': {
                    'id': other_user.id,
                    'nickname': other_user.nickname,
                    'avatar': other_user.avatar.url if other_user.avatar else None
                },
                'last_message': last_msg.content[:50] if last_msg else '',
                'last_message_time': last_msg.created_at if last_msg else None,
                'unread_count': unread_count
            })
        
        # 按最后消息时间排序
        conversations.sort(key=lambda x: x['last_message_time'] or '', reverse=True)
        
        return Response(conversations)


@extend_schema(
    tags=["私信"],
    summary="获取与指定用户的消息记录",
    description="获取与指定用户的私信记录，按时间顺序排列。同时将未读消息标记为已读。",
)
class MessageHistoryView(generics.ListAPIView):
    """消息记录接口"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs.get('user_id')
        
        # 获取与该用户的所有消息
        return Message.objects.filter(
            (Q(sender=user) & Q(receiver_id=other_user_id)) |
            (Q(sender_id=other_user_id) & Q(receiver=user))
        ).order_by('created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # 将收到的未读消息标记为已读
        other_user_id = self.kwargs.get('user_id')
        Message.objects.filter(
            sender_id=other_user_id,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=["私信"],
    summary="获取未读消息数",
    description="获取当前用户的未读私信总数。",
)
class UnreadCountView(generics.GenericAPIView):
    """未读消息数接口"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        count = Message.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
        return Response({'unread_count': count})
