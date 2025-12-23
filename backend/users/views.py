from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (
    CurrentUserSerializer,
    PhoneChangeSerializer,
    PhoneTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
)


@extend_schema(
    tags=["认证"],
    summary="用户注册",
    description="使用手机号、用户名、昵称和密码注册新用户账号。",
    examples=[
        OpenApiExample(
            "注册示例",
            value={
                "phone": "13812345678",
                "username": "testuser",
                "nickname": "测试用户",
                "password": "securePassword123"
            },
            request_only=True,
        ),
    ],
)
class RegisterView(generics.CreateAPIView):
    """用户注册接口"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    tags=["认证"],
    summary="用户登录",
    description="使用手机号和密码登录，获取 JWT Token。",
    examples=[
        OpenApiExample(
            "登录示例",
            value={
                "phone": "13812345678",
                "password": "securePassword123"
            },
            request_only=True,
        ),
    ],
)
class LoginView(TokenObtainPairView):
    """用户登录接口，返回 access 和 refresh token"""
    serializer_class = PhoneTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    tags=["认证"],
    summary="用户登出",
    description="使用 refresh_token 登出，将 token 加入黑名单。",
    examples=[
        OpenApiExample(
            "登出示例",
            value={"refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."},
            request_only=True,
        ),
    ],
)
class LogoutView(generics.GenericAPIView):
    """用户登出接口"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "缺少 refresh_token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "refresh_token 无效"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "已退出登录"})


@extend_schema_view(
    get=extend_schema(
        tags=["用户"],
        summary="获取当前用户信息",
        description="获取当前登录用户的详细信息。",
    ),
    put=extend_schema(
        tags=["用户"],
        summary="更新用户信息（全量）",
        description="更新当前用户的全部可编辑信息。",
    ),
    patch=extend_schema(
        tags=["用户"],
        summary="更新用户信息（部分）",
        description="更新当前用户的部分信息。",
    ),
)
class CurrentUserView(generics.RetrieveUpdateAPIView):
    """当前用户信息接口"""
    serializer_class = CurrentUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
    tags=["用户"],
    summary="更换手机号",
    description="验证当前密码后更换绑定的手机号。",
    examples=[
        OpenApiExample(
            "换绑手机示例",
            value={
                "password": "currentPassword123",
                "new_phone": "13987654321"
            },
            request_only=True,
        ),
    ],
)
class PhoneChangeView(generics.GenericAPIView):
    """更换手机号接口"""
    serializer_class = PhoneChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "手机号已更新"})


@extend_schema(
    tags=["用户"],
    summary="获取用户资料",
    description="根据用户ID获取用户的公开资料信息，包括好友关系状态。",
)
class UserProfileView(generics.RetrieveAPIView):
    """用户资料接口"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

