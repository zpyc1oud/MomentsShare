from datetime import datetime

from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import generics, permissions
from rest_framework.response import Response

from friends.models import Friendship
from .models import Moment, Tag
from .serializers import MomentCreateSerializer, MomentDetailSerializer, MomentListSerializer
from .utils import match_pinyin


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
        ids.add(user.id)
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
@extend_schema(
    tags=["动态"],
    summary="我的动态列表",
    description="获取当前用户发布的所有动态，按时间倒序排列，支持分页。",
)
class MyMomentsView(generics.ListAPIView):
    """我的动态列表接口"""
    serializer_class = MomentListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Moment.objects.filter(author=user, is_deleted=False)
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
        
        # 日期过滤
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
        
        # 标签过滤（支持拼音匹配）
        if label:
            # 先尝试直接匹配
            tag_qs = qs.filter(tags__name=label)
            if tag_qs.exists():
                qs = tag_qs
            else:
                # 如果直接匹配失败，尝试拼音匹配
                all_tags = Tag.objects.all()
                matching_tag_names = [tag.name for tag in all_tags if match_pinyin(label, tag.name)]
                if matching_tag_names:
                    qs = qs.filter(tags__name__in=matching_tag_names)
                else:
                    qs = qs.none()
        
        # 关键词过滤（支持拼音匹配）
        if keyword:
            # 先尝试直接匹配
            direct_matches = qs.filter(content__icontains=keyword)
            direct_ids = set(direct_matches.values_list('id', flat=True))
            
            # 判断是否需要拼音匹配
            # 1. 纯字母输入（可能是拼音）
            # 2. 直接匹配结果为空或很少
            is_pinyin_query = keyword.isalpha() and len(keyword) <= 20
            need_pinyin_match = is_pinyin_query or len(direct_ids) < 10
            
            if need_pinyin_match:
                # 从所有记录中查找拼音匹配（不限制在直接匹配结果中）
                # 为了提高性能，限制候选数量
                candidates_qs = qs.order_by("-created_at")[:1000]  # 增加候选数量
                candidates = list(candidates_qs)
                
                # 进行拼音匹配
                pinyin_matches = []
                for m in candidates:
                    if m.content and match_pinyin(keyword, m.content):
                        pinyin_matches.append(m)
                
                if pinyin_matches:
                    # 合并直接匹配和拼音匹配的结果
                    pinyin_ids = [m.id for m in pinyin_matches]
                    all_ids = list(direct_ids | set(pinyin_ids))
                    qs = Moment.objects.filter(id__in=all_ids)
                elif direct_ids:
                    # 只有直接匹配结果
                    qs = direct_matches
                else:
                    # 都没有匹配，返回空结果
                    qs = Moment.objects.none()
            else:
                # 不需要拼音匹配，直接使用直接匹配结果
                qs = direct_matches
        
        return qs.order_by("-created_at")


@extend_schema(
    tags=["动态"],
    summary="搜索建议",
    description="根据输入的关键词返回搜索建议，包括匹配的内容片段和标签。",
    parameters=[
        OpenApiParameter(
            name="q",
            type=str,
            location=OpenApiParameter.QUERY,
            description="搜索关键词",
            required=True,
        ),
        OpenApiParameter(
            name="limit",
            type=int,
            location=OpenApiParameter.QUERY,
            description="返回建议数量限制（默认10）",
            required=False,
        ),
    ],
)
class SearchSuggestionsView(generics.GenericAPIView):
    """搜索建议接口"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        limit = int(request.query_params.get("limit", 10))
        
        if not query or len(query) < 1:
            return Response({
                "suggestions": [],
                "tags": []
            })
        
        suggestions = []
        tags = []
        
        # 获取匹配的动态内容片段（支持拼音匹配）
        # 先获取所有可能的记录
        base_qs = Moment.objects.filter(
            is_deleted=False
        ).filter(
            Q(type=Moment.MomentType.IMAGE) | Q(video_status=Moment.VideoStatus.READY)
        )
        
        # 先尝试直接匹配
        direct_moments = list(base_qs.filter(content__icontains=query).order_by("-created_at")[:limit])
        direct_ids = {m.id for m in direct_moments}
        
        # 判断是否需要拼音匹配
        is_pinyin_query = query.isalpha() and len(query) <= 20
        need_pinyin_match = is_pinyin_query or len(direct_moments) < limit
        
        if need_pinyin_match:
            # 从所有记录中查找拼音匹配
            candidates = list(base_qs.order_by("-created_at")[:500])  # 增加候选数量
            pinyin_matches = []
            for m in candidates:
                if m.id not in direct_ids and m.content and match_pinyin(query, m.content):
                    pinyin_matches.append(m)
                    if len(pinyin_matches) >= limit:
                        break
            
            # 合并结果
            moments = direct_moments + pinyin_matches[:limit - len(direct_moments)]
        else:
            moments = direct_moments
        
        for moment in moments:
            if moment.content:
                # 提取包含关键词的内容片段
                content = moment.content
                # 尝试找到匹配位置（支持拼音）
                idx = -1
                query_lower = query.lower()
                content_lower = content.lower()
                
                # 先尝试直接匹配
                idx = content_lower.find(query_lower)
                
                # 如果没找到，尝试在拼音中查找
                if idx == -1:
                    from .utils import get_pinyin, get_pinyin_initials
                    content_pinyin = get_pinyin(content).lower()
                    content_initials = get_pinyin_initials(content).lower()
                    
                    # 在拼音全拼中查找
                    pinyin_idx = content_pinyin.find(query_lower)
                    if pinyin_idx != -1:
                        # 找到拼音位置，尝试映射回原文位置（简化处理）
                        idx = 0  # 简化处理，从开头显示
                    
                    # 在首字母中查找
                    if idx == -1:
                        initials_idx = content_initials.find(query_lower)
                        if initials_idx != -1:
                            idx = 0
                
                if idx != -1:
                    # 提取关键词前后各30个字符
                    start = max(0, idx - 30)
                    end = min(len(content), idx + len(query) + 30)
                    snippet = content[start:end]
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(content):
                        snippet = snippet + "..."
                    suggestions.append({
                        "text": snippet,
                        "keyword": query,
                        "moment_id": moment.id
                    })
        
        # 获取匹配的标签（支持拼音匹配）
        all_tags = Tag.objects.all()
        matching_tags = []
        
        # 先尝试直接匹配
        direct_matches = [tag for tag in all_tags if query.lower() in tag.name.lower()]
        matching_tags.extend(direct_matches)
        
        # 如果结果不足，尝试拼音匹配
        if len(matching_tags) < limit:
            pinyin_matches = [tag for tag in all_tags if match_pinyin(query, tag.name) and tag not in matching_tags]
            matching_tags.extend(pinyin_matches)
        
        tags = [{"id": tag.id, "name": tag.name} for tag in matching_tags[:limit]]
        
        return Response({
            "suggestions": suggestions[:limit],
            "tags": tags
        })


@extend_schema(
    tags=["动态"],
    summary="热门搜索",
    description="获取热门搜索标签和关键词。",
)
class HotSearchView(generics.GenericAPIView):
    """热门搜索接口"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 获取使用频率最高的标签（通过MomentTag关联统计）
        from django.db.models import Count
        hot_tags = Tag.objects.filter(
            moments__is_deleted=False
        ).annotate(
            usage_count=Count('moments', distinct=True)
        ).order_by('-usage_count', '-id')[:10]
        
        tags = [{"id": tag.id, "name": tag.name, "count": tag.usage_count} for tag in hot_tags]
        
        return Response({
            "tags": tags
        })
