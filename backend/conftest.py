"""
Shared pytest fixtures for MomentsShare tests.
"""
import io
from datetime import timedelta

import pytest
from django.utils import timezone
from PIL import Image as PILImage
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    """Return an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Create and return a regular test user."""
    from users.models import User
    return User.objects.create_user(
        phone="13800000001",
        username="testuser",
        nickname="测试用户",
        password="TestPass123!",
    )


@pytest.fixture
def user2(db):
    """Create and return a second test user."""
    from users.models import User
    return User.objects.create_user(
        phone="13800000002",
        username="testuser2",
        nickname="测试用户2",
        password="TestPass123!",
    )


@pytest.fixture
def admin_user(db):
    """Create and return an admin user."""
    from users.models import User
    return User.objects.create_user(
        phone="13800000099",
        username="adminuser",
        nickname="管理员",
        password="AdminPass123!",
        is_staff=True,
    )


@pytest.fixture
def auth_client(api_client, user):
    """Return an authenticated API client for regular user."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return api_client


@pytest.fixture
def auth_client2(api_client, user2):
    """Return an authenticated API client for second user."""
    client = APIClient()
    refresh = RefreshToken.for_user(user2)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Return an authenticated API client for admin user."""
    client = APIClient()
    refresh = RefreshToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def test_image():
    """Create a simple test image file."""
    img = PILImage.new("RGB", (100, 100), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    buffer.name = "test.jpg"
    return buffer


@pytest.fixture
def test_image_png():
    """Create a simple test PNG image file."""
    img = PILImage.new("RGB", (100, 100), color="blue")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    buffer.name = "test.png"
    return buffer


@pytest.fixture
def test_video():
    """Create a simple test video file (mock)."""
    buffer = io.BytesIO(b"fake video content")
    buffer.name = "test.mp4"
    return buffer


@pytest.fixture
def moment_image(db, user):
    """Create an IMAGE type moment."""
    from moments.models import Moment
    return Moment.objects.create(
        author=user,
        content="测试图文动态",
        type=Moment.MomentType.IMAGE,
        video_status=Moment.VideoStatus.READY,
    )


@pytest.fixture
def moment_video(db, user):
    """Create a VIDEO type moment with READY status."""
    from moments.models import Moment
    return Moment.objects.create(
        author=user,
        content="测试视频动态",
        type=Moment.MomentType.VIDEO,
        video_status=Moment.VideoStatus.READY,
    )


@pytest.fixture
def moment_video_processing(db, user):
    """Create a VIDEO type moment with PROCESSING status."""
    from moments.models import Moment
    return Moment.objects.create(
        author=user,
        content="处理中的视频",
        type=Moment.MomentType.VIDEO,
        video_status=Moment.VideoStatus.PROCESSING,
    )


@pytest.fixture
def friendship_accepted(db, user, user2):
    """Create an accepted friendship between user and user2."""
    from friends.models import Friendship
    return Friendship.objects.create(
        from_user=user,
        to_user=user2,
        status=Friendship.Status.ACCEPTED,
    )


@pytest.fixture
def friendship_pending(db, user, user2):
    """Create a pending friendship request from user to user2."""
    from friends.models import Friendship
    return Friendship.objects.create(
        from_user=user,
        to_user=user2,
        status=Friendship.Status.PENDING,
    )

