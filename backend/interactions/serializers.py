from rest_framework import serializers

from users.serializers import UserInfoSerializer
from .models import Comment, Rating, Like


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


class LikeSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "moment", "user", "created_at"]
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        user = self.context['request'].user
        moment = validated_data['moment']

        # 检查是否已经点赞，如果已点赞则取消点赞（删除）
        like_instance = Like.objects.filter(moment=moment, user=user).first()

        if like_instance:
            # 取消点赞
            like_instance.delete()
            return None  # 返回None表示取消点赞
        else:
            # 点赞
            like = Like.objects.create(moment=moment, user=user)
            return like  # 返回Like对象表示点赞成功
