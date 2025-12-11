"""
Tests for users module - covers all branches.
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestRegister:
    """Tests for user registration (U-01)."""

    def test_register_success(self, api_client):
        """Test successful registration with valid data."""
        url = "/api/v1/auth/register/"
        data = {
            "phone": "13900000001",
            "username": "newuser",
            "nickname": "新用户",
            "password": "StrongPass123!",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data

    def test_register_duplicate_phone(self, api_client, user):
        """Test registration fails with duplicate phone."""
        url = "/api/v1/auth/register/"
        data = {
            "phone": user.phone,  # Duplicate
            "username": "anotheruser",
            "nickname": "另一个用户",
            "password": "StrongPass123!",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "phone" in str(response.data) or "手机号已注册" in str(response.data)

    def test_register_duplicate_username(self, api_client, user):
        """Test registration fails with duplicate username."""
        url = "/api/v1/auth/register/"
        data = {
            "phone": "13900000002",
            "username": user.username,  # Duplicate
            "nickname": "另一个用户",
            "password": "StrongPass123!",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in str(response.data) or "用户名已存在" in str(response.data)

    def test_register_weak_password(self, api_client):
        """Test registration fails with weak password."""
        url = "/api/v1/auth/register/"
        data = {
            "phone": "13900000003",
            "username": "weakpassuser",
            "nickname": "弱密码用户",
            "password": "123",  # Too weak
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    """Tests for user login (U-03)."""

    def test_login_success(self, api_client, user):
        """Test successful login."""
        url = "/api/v1/auth/login/"
        data = {
            "phone": user.phone,
            "password": "TestPass123!",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data
        assert "user_info" in response.data

    def test_login_wrong_password(self, api_client, user):
        """Test login fails with wrong password."""
        url = "/api/v1/auth/login/"
        data = {
            "phone": user.phone,
            "password": "WrongPassword123!",
        }
        response = api_client.post(url, data)
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED]

    def test_login_nonexistent_phone(self, api_client):
        """Test login fails with non-existent phone."""
        url = "/api/v1/auth/login/"
        data = {
            "phone": "19999999999",
            "password": "AnyPassword123!",
        }
        response = api_client.post(url, data)
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED]

    def test_login_inactive_user(self, api_client, db):
        """Test login fails for inactive user."""
        from users.models import User
        inactive_user = User.objects.create_user(
            phone="13800000088",
            username="inactiveuser",
            nickname="非活跃用户",
            password="TestPass123!",
            is_active=False,
        )
        url = "/api/v1/auth/login/"
        data = {
            "phone": inactive_user.phone,
            "password": "TestPass123!",
        }
        response = api_client.post(url, data)
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED]


@pytest.mark.django_db
class TestLogout:
    """Tests for user logout (U-04)."""

    def test_logout_success(self, auth_client, user):
        """Test successful logout."""
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        url = "/api/v1/auth/logout/"
        data = {"refresh_token": str(refresh)}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK

    def test_logout_missing_token(self, auth_client):
        """Test logout fails without refresh_token."""
        url = "/api/v1/auth/logout/"
        response = auth_client.post(url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_invalid_token(self, auth_client):
        """Test logout fails with invalid refresh_token."""
        url = "/api/v1/auth/logout/"
        data = {"refresh_token": "invalid-token"}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCurrentUser:
    """Tests for current user info (U-02)."""

    def test_get_current_user(self, auth_client, user):
        """Test getting current user info."""
        url = "/api/v1/users/me/"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["phone"] == user.phone
        assert response.data["username"] == user.username

    def test_update_nickname(self, auth_client, user):
        """Test updating nickname."""
        url = "/api/v1/users/me/"
        data = {"nickname": "新昵称"}
        response = auth_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.nickname == "新昵称"

    def test_update_username_success(self, auth_client, user):
        """Test updating username successfully."""
        url = "/api/v1/users/me/"
        data = {"username": "newusername"}
        response = auth_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.username == "newusername"

    def test_update_username_duplicate(self, auth_client, user, user2):
        """Test updating username fails with duplicate."""
        url = "/api/v1/users/me/"
        data = {"username": user2.username}  # Duplicate
        response = auth_client.patch(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unauthenticated_access(self, api_client):
        """Test unauthenticated access is denied."""
        url = "/api/v1/users/me/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPhoneChange:
    """Tests for phone change (U-02-d)."""

    def test_phone_change_success(self, auth_client, user):
        """Test successful phone change."""
        url = "/api/v1/users/me/phone/"
        data = {
            "password": "TestPass123!",
            "new_phone": "13900009999",
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.phone == "13900009999"

    def test_phone_change_wrong_password(self, auth_client, user):
        """Test phone change fails with wrong password."""
        url = "/api/v1/users/me/phone/"
        data = {
            "password": "WrongPassword!",
            "new_phone": "13900009999",
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_phone_change_duplicate_phone(self, auth_client, user, user2):
        """Test phone change fails with duplicate phone."""
        url = "/api/v1/users/me/phone/"
        data = {
            "password": "TestPass123!",
            "new_phone": user2.phone,  # Duplicate
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserManager:
    """Tests for UserManager."""

    def test_create_user_without_phone(self):
        """Test creating user without phone raises error."""
        from users.models import User
        with pytest.raises(ValueError, match="Phone is required"):
            User.objects.create_user(
                phone=None,
                username="test",
                nickname="test",
                password="test",
            )

    def test_create_user_without_username(self):
        """Test creating user without username raises error."""
        from users.models import User
        with pytest.raises(ValueError, match="Username is required"):
            User.objects.create_user(
                phone="13800000001",
                username=None,
                nickname="test",
                password="test",
            )

    def test_create_user_without_nickname(self):
        """Test creating user without nickname raises error."""
        from users.models import User
        with pytest.raises(ValueError, match="Nickname is required"):
            User.objects.create_user(
                phone="13800000001",
                username="test",
                nickname=None,
                password="test",
            )

    def test_create_superuser(self, db):
        """Test creating superuser."""
        from users.models import User
        admin = User.objects.create_superuser(
            phone="13800000077",
            username="superadmin",
            nickname="超级管理员",
            password="AdminPass123!",
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.is_active is True


@pytest.mark.django_db
class TestPhoneAuthBackend:
    """Tests for PhoneAuthBackend."""

    def test_authenticate_success(self, user):
        """Test successful authentication."""
        from users.backends import PhoneAuthBackend
        backend = PhoneAuthBackend()
        result = backend.authenticate(None, phone=user.phone, password="TestPass123!")
        assert result == user

    def test_authenticate_with_username_kwarg(self, user):
        """Test authentication with username kwarg (fallback)."""
        from users.backends import PhoneAuthBackend
        backend = PhoneAuthBackend()
        result = backend.authenticate(None, username=user.phone, password="TestPass123!")
        assert result == user

    def test_authenticate_wrong_password(self, user):
        """Test authentication fails with wrong password."""
        from users.backends import PhoneAuthBackend
        backend = PhoneAuthBackend()
        result = backend.authenticate(None, phone=user.phone, password="WrongPass!")
        assert result is None

    def test_authenticate_nonexistent_user(self, db):
        """Test authentication fails for non-existent user."""
        from users.backends import PhoneAuthBackend
        backend = PhoneAuthBackend()
        result = backend.authenticate(None, phone="19999999999", password="AnyPass!")
        assert result is None

    def test_authenticate_no_phone_no_username(self, db):
        """Test authentication fails without phone or username."""
        from users.backends import PhoneAuthBackend
        backend = PhoneAuthBackend()
        result = backend.authenticate(None, password="AnyPass!")
        assert result is None

    def test_authenticate_no_password(self, user):
        """Test authentication fails without password."""
        from users.backends import PhoneAuthBackend
        backend = PhoneAuthBackend()
        result = backend.authenticate(None, phone=user.phone, password=None)
        assert result is None

    def test_get_user_exists(self, user):
        """Test getting existing user."""
        from users.backends import PhoneAuthBackend
        backend = PhoneAuthBackend()
        result = backend.get_user(user.id)
        assert result == user

    def test_get_user_not_exists(self, db):
        """Test getting non-existent user."""
        from users.backends import PhoneAuthBackend
        backend = PhoneAuthBackend()
        result = backend.get_user(99999)
        assert result is None

