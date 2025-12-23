from rest_framework import serializers

# 1. 修改导入：引入我们新建的 DFA 过滤器实例 gfw
from core.dfa_filter import gfw
from users.serializers import UserInfoSerializer
from .models import Image, Moment, Tag
from .tasks import transcode_video


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image_file", "order"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class MomentCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), allow_empty=True, required=False, write_only=True
    )
    video = serializers.FileField(required=False, allow_null=True, write_only=True)
    labels = serializers.ListField(
        child=serializers.CharField(max_length=10), allow_empty=True, required=False, write_only=True
    )

    class Meta:
        model = Moment
        fields = ["id", "content", "type", "images", "video", "labels"]

    def validate(self, attrs):
        moment_type = attrs.get("type")
        images = self.initial_data.getlist("images") if hasattr(self.initial_data, "getlist") else attrs.get("images")
        video = attrs.get("video")
        content = attrs.get("content", "")
        labels = attrs.get("labels", [])

        # 2. 修改验证逻辑：使用 DFA 算法检测
        # gfw.exists 返回两个值：(是否敏感, 敏感词是什么)
        is_sensitive, word = gfw.exists(content)
        if is_sensitive:
            # 可以在这里把 word 打印到日志里方便调试，但返回给用户时建议模糊处理
            # print(f"拦截敏感词: {word}")
            raise serializers.ValidationError({"content": f"发布失败：内容包含违规信息，请文明发言。"})

        # 3. 新增：标签敏感词检查
        if labels:
            sensitive_labels = []
            for label in labels:
                is_label_sensitive, sensitive_word = gfw.exists(label)
                if is_label_sensitive:
                    sensitive_labels.append(f"#{label}")

            if sensitive_labels:
                label_list = "、".join(sensitive_labels)
                raise serializers.ValidationError({
                    "labels": f"发布失败：标签 {label_list} 包含违规信息，请修改后重试。"
                })

        if moment_type == Moment.MomentType.IMAGE:
            if video:
                raise serializers.ValidationError({"video": "图文动态不能上传视频"})
            if images is None:
                images = []
            if len(images) > 9:
                raise serializers.ValidationError({"images": "图片最多9张"})
        elif moment_type == Moment.MomentType.VIDEO:
            if images:
                raise serializers.ValidationError({"images": "视频动态不能上传图片"})
            if not video:
                raise serializers.ValidationError({"video": "视频动态需要上传视频文件"})
        else:
            raise serializers.ValidationError({"type": "无效的动态类型"})
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        images = request.FILES.getlist("images")
        video = validated_data.pop("video", None)
        labels = validated_data.pop("labels", [])
        validated_data.pop("images", None)
        validated_data["author"] = request.user
        moment = Moment.objects.create(**validated_data)

        # Handle tags
        for name in labels or []:
            tag, _ = Tag.objects.get_or_create(name=name[:10])
            moment.tags.add(tag)

        # Handle media
        if moment.type == Moment.MomentType.IMAGE:
            for idx, img in enumerate(images or [], start=1):
                Image.objects.create(moment=moment, image_file=img, order=idx)
            moment.video_status = Moment.VideoStatus.READY
        else:
            moment.video_file = video
            moment.video_status = Moment.VideoStatus.PROCESSING
            moment.save(update_fields=["video_file", "video_status"])
            # trigger async task
            transcode_video.delay(moment.id)
        moment.save()
        return moment


class MomentListSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Moment
        fields = [
            "id",
            "author",
            "content",
            "type",
            "video_file",
            "video_status",
            "is_deleted",
            "created_at",
            "images",
            "tags",
            "likes_count",
            "is_liked",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class MomentDetailSerializer(MomentListSerializer):
    class Meta(MomentListSerializer.Meta):
        fields = MomentListSerializer.Meta.fields