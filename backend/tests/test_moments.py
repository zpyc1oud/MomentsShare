"""
Tests for moments module - covers all branches.
"""
import io
import pytest
from unittest.mock import patch
from PIL import Image as PILImage
from rest_framework import status


@pytest.mark.django_db
class TestMomentCreate:
    """Tests for moment creation (C-01)."""

    def test_create_image_moment_success(self, auth_client, test_image):
        """Test creating image moment successfully."""
        url = "/api/v1/moments/"
        data = {
            "type": "IMAGE",
            "content": "测试图文动态",
            "images": [test_image],
        }
        response = auth_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["type"] == "IMAGE"

    def test_create_image_moment_no_images(self, auth_client):
        """Test creating image moment without images (allowed)."""
        url = "/api/v1/moments/"
        data = {
            "type": "IMAGE",
            "content": "纯文字动态",
        }
        response = auth_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_image_moment_too_many_images(self, auth_client):
        """Test creating image moment with more than 9 images fails."""
        url = "/api/v1/moments/"
        images = []
        for i in range(10):
            img = PILImage.new("RGB", (50, 50), color="green")
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            buf.seek(0)
            buf.name = f"img{i}.jpg"
            images.append(buf)
        data = {
            "type": "IMAGE",
            "content": "太多图片",
            "images": images,
        }
        response = auth_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "9" in str(response.data) or "images" in str(response.data)

    def test_create_image_moment_with_video_fails(self, auth_client, test_video):
        """Test creating image moment with video fails."""
        url = "/api/v1/moments/"
        data = {
            "type": "IMAGE",
            "content": "图文但带视频",
            "video": test_video,
        }
        response = auth_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch("moments.serializers.transcode_video.delay")
    def test_create_video_moment_success(self, mock_delay, auth_client, test_video):
        """Test creating video moment successfully."""
        url = "/api/v1/moments/"
        data = {
            "type": "VIDEO",
            "content": "测试视频动态",
            "video": test_video,
        }
        response = auth_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["type"] == "VIDEO"
        mock_delay.assert_called_once()

    def test_create_video_moment_without_video_fails(self, auth_client):
        """Test creating video moment without video fails."""
        url = "/api/v1/moments/"
        data = {
            "type": "VIDEO",
            "content": "没有视频的视频动态",
        }
        response = auth_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_video_moment_with_images_fails(self, auth_client, test_image, test_video):
        """Test creating video moment with images fails."""
        url = "/api/v1/moments/"
        data = {
            "type": "VIDEO",
            "content": "视频但带图片",
            "images": [test_image],
            "video": test_video,
        }
        response = auth_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_moment_invalid_type(self, auth_client):
        """Test creating moment with invalid type fails."""
        url = "/api/v1/moments/"
        data = {
            "type": "INVALID",
            "content": "无效类型",
        }
        response = auth_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_moment_with_sensitive_content(self, auth_client, settings):
        """Test creating moment with sensitive content fails (C-04)."""
        settings.SENSITIVE_WORDS = ["违禁", "敏感", "非法"]
        url = "/api/v1/moments/"
        data = {
            "type": "IMAGE",
            "content": "这里有违禁词",
        }
        response = auth_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "敏感" in str(response.data) or "content" in str(response.data)

    def test_create_moment_with_labels(self, auth_client):
        """Test creating moment with labels."""
        url = "/api/v1/moments/"
        data = {
            "type": "IMAGE",
            "content": "带标签的动态",
            "labels": ["美食", "旅行", "日常"],
        }
        response = auth_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_moment_with_sensitive_labels(self, auth_client, settings):
        """Test creating moment with sensitive labels fails."""
        # 使用 DFA 词库中的实际敏感词（如"暴力"）
        url = "/api/v1/moments/"
        data = {
            "type": "IMAGE",
            "content": "正常内容",
            "labels": ["暴力", "美食"],  # "暴力"在敏感词库中
        }
        response = auth_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "标签" in str(response.data)
        assert "#暴力" in str(response.data)

    def test_create_moment_with_multiple_sensitive_labels(self, auth_client, settings):
        """Test creating moment with multiple sensitive labels fails."""
        url = "/api/v1/moments/"
        data = {
            "type": "IMAGE",
            "content": "正常内容",
            "labels": ["暴力", "色情"],  # 两个都是敏感词
        }
        response = auth_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "标签" in str(response.data)
        # 应该显示所有违规标签
        response_text = str(response.data)
        assert "#暴力" in response_text
        assert "#色情" in response_text

    def test_create_moment_unauthenticated(self, api_client):
        """Test creating moment without authentication fails."""
        url = "/api/v1/moments/"
        data = {
            "type": "IMAGE",
            "content": "未登录",
        }
        response = api_client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestMomentDetail:
    """Tests for moment detail (C-03 detail)."""

    def test_get_moment_detail(self, auth_client, moment_image):
        """Test getting moment detail."""
        url = f"/api/v1/moments/{moment_image.id}/"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == moment_image.id

    def test_get_deleted_moment_fails(self, auth_client, moment_image):
        """Test getting deleted moment fails."""
        moment_image.is_deleted = True
        moment_image.save()
        url = f"/api/v1/moments/{moment_image.id}/"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_processing_video_by_author(self, auth_client, user, moment_video_processing):
        """Test author can see their processing video."""
        url = f"/api/v1/moments/{moment_video_processing.id}/"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_processing_video_by_other_user(self, auth_client2, user2, moment_video_processing):
        """Test other users cannot see processing video."""
        url = f"/api/v1/moments/{moment_video_processing.id}/"
        response = auth_client2.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_nonexistent_moment(self, auth_client):
        """Test getting non-existent moment returns 404."""
        url = "/api/v1/moments/99999/"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestFeed:
    """Tests for feed (S-02)."""

    def test_feed_shows_friend_moments(self, auth_client2, user, user2, moment_image, friendship_accepted):
        """Test feed shows accepted friend's moments."""
        url = "/api/v1/moments/feed/"
        response = auth_client2.get(url)
        assert response.status_code == status.HTTP_200_OK
        ids = [m["id"] for m in response.data["results"]]
        assert moment_image.id in ids

    def test_feed_excludes_non_friend_moments(self, auth_client2, user, user2, moment_image):
        """Test feed excludes non-friend's moments."""
        # No friendship created
        url = "/api/v1/moments/feed/"
        response = auth_client2.get(url)
        assert response.status_code == status.HTTP_200_OK
        ids = [m["id"] for m in response.data["results"]]
        assert moment_image.id not in ids

    def test_feed_excludes_pending_friend_moments(self, auth_client2, user, user2, moment_image, friendship_pending):
        """Test feed excludes pending friend's moments."""
        url = "/api/v1/moments/feed/"
        response = auth_client2.get(url)
        assert response.status_code == status.HTTP_200_OK
        ids = [m["id"] for m in response.data["results"]]
        assert moment_image.id not in ids

    def test_feed_excludes_processing_videos(self, auth_client2, user, user2, moment_video_processing, friendship_accepted):
        """Test feed excludes processing videos."""
        url = "/api/v1/moments/feed/"
        response = auth_client2.get(url)
        assert response.status_code == status.HTTP_200_OK
        ids = [m["id"] for m in response.data["results"]]
        assert moment_video_processing.id not in ids

    def test_feed_shows_ready_videos(self, auth_client2, user, user2, moment_video, friendship_accepted):
        """Test feed shows ready videos."""
        url = "/api/v1/moments/feed/"
        response = auth_client2.get(url)
        assert response.status_code == status.HTTP_200_OK
        ids = [m["id"] for m in response.data["results"]]
        assert moment_video.id in ids


@pytest.mark.django_db
class TestSearch:
    """Tests for search (C-03)."""

    def test_search_by_keyword(self, auth_client, moment_image):
        """Test searching by keyword."""
        url = "/api/v1/moments/search/?keyword=测试"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        ids = [m["id"] for m in response.data["results"]]
        assert moment_image.id in ids

    def test_search_by_label(self, auth_client, db, user):
        """Test searching by label."""
        from moments.models import Moment, Tag
        tag = Tag.objects.create(name="美食")
        moment = Moment.objects.create(
            author=user,
            content="美食分享",
            type=Moment.MomentType.IMAGE,
            video_status=Moment.VideoStatus.READY,
        )
        moment.tags.add(tag)

        url = "/api/v1/moments/search/?label=美食"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        ids = [m["id"] for m in response.data["results"]]
        assert moment.id in ids

    def test_search_by_date_range(self, auth_client, moment_image):
        """Test searching by date range."""
        from datetime import date
        today = date.today().isoformat()
        url = f"/api/v1/moments/search/?start_date={today}&end_date={today}"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_search_with_invalid_date(self, auth_client):
        """Test searching with invalid date format."""
        url = "/api/v1/moments/search/?start_date=invalid"
        response = auth_client.get(url)
        # Should not crash, just ignore invalid date
        assert response.status_code == status.HTTP_200_OK

    def test_search_excludes_deleted(self, auth_client, moment_image):
        """Test search excludes deleted moments."""
        moment_image.is_deleted = True
        moment_image.save()
        url = "/api/v1/moments/search/?keyword=测试"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        ids = [m["id"] for m in response.data["results"]]
        assert moment_image.id not in ids


@pytest.mark.django_db
class TestSensitiveWords:
    """Tests for sensitive word filtering (C-04)."""

    def test_contains_sensitive_word_true(self, settings):
        """Test detecting sensitive word."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = ["违禁", "敏感"]
        assert contains_sensitive_word("这是违禁内容") is True

    def test_contains_sensitive_word_false(self, settings):
        """Test no sensitive word detected."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = ["违禁", "敏感"]
        assert contains_sensitive_word("这是正常内容") is False

    def test_contains_sensitive_word_empty(self, settings):
        """Test empty text returns False."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = ["违禁"]
        assert contains_sensitive_word("") is False
        assert contains_sensitive_word(None) is False

    def test_contains_sensitive_word_empty_list(self, settings):
        """Test empty word list."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = []
        assert contains_sensitive_word("任何内容") is False

    def test_contains_sensitive_word_empty_word_in_list(self, settings):
        """Test empty word in list is skipped."""
        from core.sensitive_words import contains_sensitive_word
        settings.SENSITIVE_WORDS = ["", "违禁"]
        assert contains_sensitive_word("违禁内容") is True
        assert contains_sensitive_word("正常内容") is False


@pytest.mark.django_db
class TestMomentModels:
    """Tests for moment models."""

    def test_moment_str(self, moment_image):
        """Test Moment __str__ method."""
        assert str(moment_image.author) in str(moment_image)

    def test_tag_str(self, db):
        """Test Tag __str__ method."""
        from moments.models import Tag
        tag = Tag.objects.create(name="测试标签")
        assert str(tag) == "测试标签"

    def test_image_str(self, db, moment_image):
        """Test Image __str__ method."""
        from moments.models import Image
        img = Image.objects.create(
            moment=moment_image,
            image_file="images/test.jpg",
            order=1,
        )
        assert "Image" in str(img)
