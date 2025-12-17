from rest_framework import serializers

from users.serializers import UserInfoSerializer
from .models import Comment, Rating


class CommentSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True)
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
                    raise serializers.ValidationError({"parent_id": "该父评论不属于该动态"})
                attrs["parent"] = parent
            except Comment.DoesNotExist:
                raise serializers.ValidationError({"parent_id": "父评论不存在"})
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "moment", "user", "score", "created_at"]
        read_only_fields = ["user", "created_at"]

    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        moment = validated_data['moment']
        score = validated_data['score']
        rating, created = Rating.objects.update_or_create(
            moment=moment, user=user,
            defaults={'score': score}
        )
        return rating
