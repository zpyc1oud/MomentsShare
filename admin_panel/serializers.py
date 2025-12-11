from rest_framework import serializers
from users.serializers import PhoneTokenObtainPairSerializer


class AdminTokenObtainPairSerializer(PhoneTokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not (user.is_staff or user.is_superuser):
            raise serializers.ValidationError({"detail": "非管理员账号禁止访问"})
        return data

