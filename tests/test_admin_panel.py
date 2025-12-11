"""
Tests for admin_panel module - covers all branches.
"""
import pytest
from datetime import date
from rest_framework import status


@pytest.mark.django_db
class TestAdminLogin:
    """Tests for admin login (A-01)."""

    def test_admin_login_success(self, api_client, admin_user):
        """Test admin login successfully."""
        url = "/api/v1/admin/auth/login/"
        data = {
            "phone": admin_user.phone,
            "password": "AdminPass123!",
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_admin_login_non_admin_user(self, api_client, user):
        """Test non-admin user cannot login to admin."""
        url = "/api/v1/admin/auth/login/"
        data = {
            "phone": user.phone,
            "password": "TestPass123!",
        }
        response = api_client.post(url, data)
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED]

    def test_admin_login_wrong_password(self, api_client, admin_user):
        """Test admin login fails with wrong password."""
        url = "/api/v1/admin/auth/login/"
        data = {
            "phone": admin_user.phone,
            "password": "WrongPassword!",
        }
        response = api_client.post(url, data)
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED]


@pytest.mark.django_db
class TestAdminContentList:
    """Tests for admin content list (A-02-a)."""

    def test_list_all_content(self, admin_client, moment_image, moment_video):
        """Test listing all content."""
        url = "/api/v1/admin/contents/"
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data

    def test_list_content_filter_by_user(self, admin_client, moment_image, user):
        """Test filtering content by user."""
        url = f"/api/v1/admin/contents/?user_id={user.id}"
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        for item in response.data["results"]:
            assert item["author"]["id"] == user.id

    def test_list_content_non_admin_denied(self, auth_client):
        """Test non-admin access is denied."""
        url = "/api/v1/admin/contents/"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_content_unauthenticated_denied(self, api_client):
        """Test unauthenticated access is denied."""
        url = "/api/v1/admin/contents/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestAdminContentDelete:
    """Tests for admin content delete (A-02-b)."""

    def test_delete_content_success(self, admin_client, moment_image):
        """Test soft deleting content successfully."""
        url = f"/api/v1/admin/contents/{moment_image.id}/"
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_200_OK

        moment_image.refresh_from_db()
        assert moment_image.is_deleted is True

    def test_delete_nonexistent_content(self, admin_client):
        """Test deleting non-existent content fails."""
        url = "/api/v1/admin/contents/99999/"
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_content_non_admin_denied(self, auth_client, moment_image):
        """Test non-admin cannot delete content."""
        url = f"/api/v1/admin/contents/{moment_image.id}/"
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestAdminStats:
    """Tests for admin stats (A-03)."""

    def test_get_stats(self, admin_client):
        """Test getting stats."""
        url = "/api/v1/admin/stats/"
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "dau" in response.data
        assert "daily_new_users" in response.data
        assert "daily_posts" in response.data

    def test_stats_counts_today_data(self, admin_client, user, moment_image, db):
        """Test stats counts today's data correctly."""
        from users.models import User
        from moments.models import Moment
        from interactions.models import Comment

        # Create today's data
        today_user = User.objects.create_user(
            phone="13800000055",
            username="todayuser",
            nickname="今日用户",
            password="TestPass123!",
        )

        url = "/api/v1/admin/stats/"
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["daily_new_users"] >= 1

    def test_stats_non_admin_denied(self, auth_client):
        """Test non-admin access is denied."""
        url = "/api/v1/admin/stats/"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestIsStaffUserPermission:
    """Tests for IsStaffUser permission."""

    def test_permission_allows_staff(self, admin_user):
        """Test permission allows staff user."""
        from admin_panel.permissions import IsStaffUser
        from rest_framework.test import APIRequestFactory

        permission = IsStaffUser()
        factory = APIRequestFactory()
        request = factory.get("/")
        request.user = admin_user

        assert permission.has_permission(request, None) is True

    def test_permission_allows_superuser(self, db):
        """Test permission allows superuser."""
        from users.models import User
        from admin_panel.permissions import IsStaffUser
        from rest_framework.test import APIRequestFactory

        superuser = User.objects.create_superuser(
            phone="13800000066",
            username="superuser",
            nickname="超级用户",
            password="SuperPass123!",
        )

        permission = IsStaffUser()
        factory = APIRequestFactory()
        request = factory.get("/")
        request.user = superuser

        assert permission.has_permission(request, None) is True

    def test_permission_denies_regular_user(self, user):
        """Test permission denies regular user."""
        from admin_panel.permissions import IsStaffUser
        from rest_framework.test import APIRequestFactory

        permission = IsStaffUser()
        factory = APIRequestFactory()
        request = factory.get("/")
        request.user = user

        assert permission.has_permission(request, None) is False

    def test_permission_denies_unauthenticated(self):
        """Test permission denies unauthenticated request."""
        from admin_panel.permissions import IsStaffUser
        from rest_framework.test import APIRequestFactory
        from django.contrib.auth.models import AnonymousUser

        permission = IsStaffUser()
        factory = APIRequestFactory()
        request = factory.get("/")
        request.user = AnonymousUser()

        assert permission.has_permission(request, None) is False


@pytest.mark.django_db
class TestAdminTokenSerializer:
    """Tests for AdminTokenObtainPairSerializer."""

    def test_serializer_rejects_non_admin(self, db, user):
        """Test serializer rejects non-admin user."""
        from admin_panel.serializers import AdminTokenObtainPairSerializer
        from rest_framework.test import APIRequestFactory

        factory = APIRequestFactory()
        request = factory.post("/")

        serializer = AdminTokenObtainPairSerializer(
            data={"phone": user.phone, "password": "TestPass123!"},
            context={"request": request},
        )

        # Validation should fail for non-admin
        assert not serializer.is_valid() or "非管理员" in str(serializer.errors)

