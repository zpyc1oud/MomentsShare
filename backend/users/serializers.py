from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "phone", "username", "nickname", "password", "avatar"]

    def validate(self, attrs):
        phone = attrs.get("phone")
        username = attrs.get("username")
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({"phone": "该手机号已注册"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "用户名已存在"})
        validate_password(attrs.get("password"))
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname", "avatar"]


class UserSerializer(serializers.ModelSerializer):
    friendship_status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "nickname", "phone", "avatar", "friendship_status"]
        read_only_fields = ["id"]

    def get_friendship_status(self, obj):
        """获取当前用户与该用户的好友关系状态"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None

        user = request.user
        if obj.id == user.id:
            return None

        from friends.models import Friendship
        friendship = Friendship.objects.filter(
            (Q(from_user=user) & Q(to_user=obj)) |
            (Q(from_user=obj) & Q(to_user=user))
        ).first()

        if friendship:
            return friendship.status
        return None


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "username", "nickname", "avatar", "created_at"]
        read_only_fields = ["id", "phone", "created_at"]

    def validate_username(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value


class PhoneChangeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_phone = serializers.CharField(max_length=11)

    def validate(self, attrs):
        user = self.context["request"].user
        password = attrs.get("password")
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "密码验证失败"})
        new_phone = attrs.get("new_phone")
        if User.objects.filter(phone=new_phone).exclude(pk=user.pk).exists():
            raise serializers.ValidationError({"new_phone": "该手机号已注册"})
        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.phone = self.validated_data["new_phone"]
        user.save(update_fields=["phone"])
        return user


class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "phone"

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")
        user = authenticate(request=self.context.get("request"), phone=phone, password=password)
        if user is None:
            raise serializers.ValidationError({"detail": "手机号或密码错误"})
        if not user.is_active:
            raise serializers.ValidationError({"detail": "账号未激活"})
        self.user = user  # Store for subclasses
        data = super().validate({"phone": phone, "password": password})
        data["user_info"] = UserInfoSerializer(user).data
        return data

