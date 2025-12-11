from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    parent_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ["id", "moment", "author", "content", "parent", "parent_id", "created_at", "replies"]
        read_only_fields = ["author", "moment", "parent", "created_at", "replies"]

    def get_replies(self, obj):
        qs = obj.replies.filter(is_deleted=False)
        return CommentSerializer(qs, many=True).data

    def validate(self, attrs):
        parent_id = attrs.pop("parent_id", None)
        if parent_id:
            moment = self.context.get("moment")
            try:
                parent = Comment.objects.get(id=parent_id)
                if moment and parent.moment_id != moment.id:
                    raise serializers.ValidationError({"parent_id": "父评论不属于该动态"})
                attrs["parent"] = parent
            except Comment.DoesNotExist:
                raise serializers.ValidationError({"parent_id": "父评论不存在"})
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)

