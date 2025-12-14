"""
Tests for serializers - covers all branches.
"""
import io
import pytest
from PIL import Image as PILImage
from rest_framework.test import APIRequestFactory


@pytest.mark.django_db
class TestMomentCreateSerializer:
    """Tests for MomentCreateSerializer."""

    def test_validate_image_type_with_video(self, user, test_video):
        """Test validation fails for IMAGE type with video."""
        from moments.serializers import MomentCreateSerializer

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user

        serializer = MomentCreateSerializer(
            data={
                "type": "IMAGE",
                "content": "测试",
                "video": test_video,
            },
            context={"request": request},
        )
        assert not serializer.is_valid()
        assert "video" in serializer.errors

    def test_validate_video_type_with_images(self, user, test_image, test_video):
        """Test validation fails for VIDEO type with images."""
        from moments.serializers import MomentCreateSerializer

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user
        request.FILES.setlist = lambda k, v: None

        serializer = MomentCreateSerializer(
            data={
                "type": "VIDEO",
                "content": "测试",
                "images": [test_image],
                "video": test_video,
            },
            context={"request": request},
        )
        assert not serializer.is_valid()

    def test_validate_invalid_type(self, user):
        """Test validation fails for invalid type."""
        from moments.serializers import MomentCreateSerializer

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user

        serializer = MomentCreateSerializer(
            data={
                "type": "INVALID",
                "content": "测试",
            },
            context={"request": request},
        )
        assert not serializer.is_valid()

    def test_validate_sensitive_content(self, user, settings):
        """Test validation fails for sensitive content."""
        from moments.serializers import MomentCreateSerializer
        settings.SENSITIVE_WORDS = ["违禁"]

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user

        serializer = MomentCreateSerializer(
            data={
                "type": "IMAGE",
                "content": "这是违禁内容",
            },
            context={"request": request},
        )
        assert not serializer.is_valid()
        assert "content" in serializer.errors


@pytest.mark.django_db
class TestRegisterSerializer:
    """Tests for RegisterSerializer."""

    def test_validate_duplicate_phone(self, user):
        """Test validation fails for duplicate phone."""
        from users.serializers import RegisterSerializer

        serializer = RegisterSerializer(
            data={
                "phone": user.phone,  # Duplicate
                "username": "newuser",
                "nickname": "新用户",
                "password": "StrongPass123!",
            }
        )
        assert not serializer.is_valid()
        assert "phone" in str(serializer.errors)

    def test_validate_duplicate_username(self, user):
        """Test validation fails for duplicate username."""
        from users.serializers import RegisterSerializer

        serializer = RegisterSerializer(
            data={
                "phone": "13900001111",
                "username": user.username,  # Duplicate
                "nickname": "新用户",
                "password": "StrongPass123!",
            }
        )
        assert not serializer.is_valid()
        assert "username" in str(serializer.errors)

    def test_create_user_success(self, db):
        """Test creating user successfully."""
        from users.serializers import RegisterSerializer

        serializer = RegisterSerializer(
            data={
                "phone": "13900002222",
                "username": "brandnewuser",
                "nickname": "全新用户",
                "password": "StrongPass123!",
            }
        )
        assert serializer.is_valid()
        user = serializer.save()
        assert user.phone == "13900002222"
        assert user.username == "brandnewuser"


@pytest.mark.django_db
class TestCurrentUserSerializer:
    """Tests for CurrentUserSerializer."""

    def test_validate_username_unique(self, user, user2):
        """Test username uniqueness validation."""
        from users.serializers import CurrentUserSerializer

        serializer = CurrentUserSerializer(
            instance=user,
            data={"username": user2.username},  # Duplicate
            partial=True,
        )
        assert not serializer.is_valid()


@pytest.mark.django_db
class TestPhoneChangeSerializer:
    """Tests for PhoneChangeSerializer."""

    def test_validate_wrong_password(self, user):
        """Test validation fails for wrong password."""
        from users.serializers import PhoneChangeSerializer
        from rest_framework.test import APIRequestFactory

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user

        serializer = PhoneChangeSerializer(
            data={
                "password": "WrongPassword!",
                "new_phone": "13900003333",
            },
            context={"request": request},
        )
        assert not serializer.is_valid()
        assert "password" in str(serializer.errors)

    def test_validate_duplicate_phone(self, user, user2):
        """Test validation fails for duplicate phone."""
        from users.serializers import PhoneChangeSerializer
        from rest_framework.test import APIRequestFactory

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user

        serializer = PhoneChangeSerializer(
            data={
                "password": "TestPass123!",
                "new_phone": user2.phone,  # Duplicate
            },
            context={"request": request},
        )
        assert not serializer.is_valid()
        assert "new_phone" in str(serializer.errors)

    def test_save_updates_phone(self, user):
        """Test saving updates phone successfully."""
        from users.serializers import PhoneChangeSerializer
        from rest_framework.test import APIRequestFactory

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = user

        serializer = PhoneChangeSerializer(
            data={
                "password": "TestPass123!",
                "new_phone": "13900004444",
            },
            context={"request": request},
        )
        assert serializer.is_valid()
        serializer.save()
        user.refresh_from_db()
        assert user.phone == "13900004444"


@pytest.mark.django_db
class TestFriendshipSerializer:
    """Tests for FriendshipSerializer."""

    def test_serialize_friendship(self, friendship_accepted):
        """Test serializing friendship."""
        from friends.serializers import FriendshipSerializer

        serializer = FriendshipSerializer(friendship_accepted)
        assert serializer.data["status"] == "ACCEPTED"
        assert "from_user" in serializer.data
        assert "to_user" in serializer.data


@pytest.mark.django_db
class TestCommentSerializer:
    """Tests for CommentSerializer."""

    def test_validate_parent_wrong_moment(self, moment_image, moment_video, db):
        """Test validation fails when parent belongs to different moment."""
        from interactions.models import Comment
        from interactions.serializers import CommentSerializer
        from rest_framework.test import APIRequestFactory

        # Create parent comment on different moment
        parent = Comment.objects.create(
            moment=moment_video,
            author=moment_video.author,
            content="另一个动态的评论",
        )

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = moment_image.author

        serializer = CommentSerializer(
            data={
                "content": "回复",
                "parent_id": parent.id,
            },
            context={"request": request, "moment": moment_image},
        )
        assert not serializer.is_valid()
        assert "parent_id" in str(serializer.errors)

    def test_validate_parent_not_exist(self, moment_image, db):
        """Test validation fails when parent does not exist."""
        from interactions.serializers import CommentSerializer
        from rest_framework.test import APIRequestFactory

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = moment_image.author

        serializer = CommentSerializer(
            data={
                "content": "回复",
                "parent_id": 99999,
            },
            context={"request": request, "moment": moment_image},
        )
        assert not serializer.is_valid()
        assert "parent_id" in str(serializer.errors)

    def test_validate_success_with_parent(self, moment_image, db):
        """Test validation succeeds with valid parent."""
        from interactions.models import Comment
        from interactions.serializers import CommentSerializer
        from rest_framework.test import APIRequestFactory

        parent = Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="父评论",
        )

        factory = APIRequestFactory()
        request = factory.post("/")
        request.user = moment_image.author

        serializer = CommentSerializer(
            data={
                "content": "回复",
                "parent_id": parent.id,
            },
            context={"request": request, "moment": moment_image},
        )
        assert serializer.is_valid()


@pytest.mark.django_db
class TestImageSerializer:
    """Tests for ImageSerializer."""

    def test_serialize_image(self, moment_image, db):
        """Test serializing image."""
        from moments.models import Image
        from moments.serializers import ImageSerializer

        img = Image.objects.create(
            moment=moment_image,
            image_file="images/test.jpg",
            order=1,
        )
        serializer = ImageSerializer(img)
        assert serializer.data["order"] == 1


@pytest.mark.django_db
class TestTagSerializer:
    """Tests for TagSerializer."""

    def test_serialize_tag(self, db):
        """Test serializing tag."""
        from moments.models import Tag
        from moments.serializers import TagSerializer

        tag = Tag.objects.create(name="测试标签")
        serializer = TagSerializer(tag)
        assert serializer.data["name"] == "测试标签"

