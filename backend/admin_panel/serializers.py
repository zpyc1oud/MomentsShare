from rest_framework import serializers
from users.serializers import PhoneTokenObtainPairSerializer
from users.models import User
from interactions.models import Comment


class AdminTokenObtainPairSerializer(PhoneTokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not (user.is_staff or user.is_superuser):
            raise serializers.ValidationError({"detail": "非管理员账号禁止访问"})
        return data


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "username", "nickname", "avatar", "is_active", "created_at", "is_staff"]


class AdminCommentListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.nickname", read_only=True)
    author_avatar = serializers.ImageField(source="author.avatar", read_only=True)
    moment_text = serializers.CharField(source="moment.content", read_only=True)
    
    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "author_id", "author_name", "author_avatar", "moment_id", "moment_text", "is_deleted"]

