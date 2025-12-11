from rest_framework import serializers

from core.sensitive_words import contains_sensitive_word
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
        if contains_sensitive_word(content):
            raise serializers.ValidationError({"content": "包含敏感内容"})
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
        ]


class MomentDetailSerializer(MomentListSerializer):
    class Meta(MomentListSerializer.Meta):
        fields = MomentListSerializer.Meta.fields

