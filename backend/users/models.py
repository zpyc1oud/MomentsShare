from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, phone, username, nickname, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone is required")
        if not username:
            raise ValueError("Username is required")
        if not nickname:
            raise ValueError("Nickname is required")
        phone = str(phone)
        user = self.model(
            phone=phone,
            username=username,
            nickname=nickname,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(phone, username, nickname, password, **extra_fields)


def default_avatar_path():
    return "default_avatar.png"


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, default=default_avatar_path)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username", "nickname"]

    def __str__(self):
        return f"{self.username}({self.phone})"

