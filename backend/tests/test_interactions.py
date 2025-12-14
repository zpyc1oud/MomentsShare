"""
Tests for interactions module - covers all branches.
"""
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestComments:
    """Tests for comments (S-03)."""

    def test_create_comment_success(self, auth_client, moment_image):
        """Test creating a comment successfully."""
        url = f"/api/v1/moments/{moment_image.id}/comments/"
        data = {"content": "这是一条评论"}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["content"] == "这是一条评论"

    def test_create_reply_success(self, auth_client, moment_image, db):
        """Test creating a reply (楼中楼) successfully."""
        from interactions.models import Comment
        parent = Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="父评论",
        )
        url = f"/api/v1/moments/{moment_image.id}/comments/"
        data = {
            "content": "这是一条回复",
            "parent_id": parent.id,
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["parent"] == parent.id

    def test_create_reply_wrong_moment(self, auth_client, moment_image, moment_video, db):
        """Test creating reply to comment from different moment fails."""
        from interactions.models import Comment
        parent = Comment.objects.create(
            moment=moment_video,  # Different moment
            author=moment_video.author,
            content="另一个动态的评论",
        )
        url = f"/api/v1/moments/{moment_image.id}/comments/"
        data = {
            "content": "尝试回复错误的评论",
            "parent_id": parent.id,
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_reply_nonexistent_parent(self, auth_client, moment_image):
        """Test creating reply to non-existent parent fails."""
        url = f"/api/v1/moments/{moment_image.id}/comments/"
        data = {
            "content": "回复不存在的评论",
            "parent_id": 99999,
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_comments(self, auth_client, moment_image, db):
        """Test listing comments."""
        from interactions.models import Comment
        Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="评论1",
        )
        Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="评论2",
        )
        url = f"/api/v1/moments/{moment_image.id}/comments/"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 2

    def test_list_comments_excludes_deleted(self, auth_client, moment_image, db):
        """Test listing comments excludes deleted ones."""
        from interactions.models import Comment
        comment = Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="已删除的评论",
            is_deleted=True,
        )
        url = f"/api/v1/moments/{moment_image.id}/comments/"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        ids = [c["id"] for c in response.data["results"]]
        assert comment.id not in ids

    def test_list_comments_with_replies(self, auth_client, moment_image, db):
        """Test listing comments includes nested replies."""
        from interactions.models import Comment
        parent = Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="父评论",
        )
        reply = Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="回复",
            parent=parent,
        )
        url = f"/api/v1/moments/{moment_image.id}/comments/"
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Parent should have replies
        parent_data = [c for c in response.data["results"] if c["id"] == parent.id][0]
        assert len(parent_data["replies"]) == 1

    def test_comment_on_deleted_moment(self, auth_client, moment_image):
        """Test commenting on deleted moment fails."""
        moment_image.is_deleted = True
        moment_image.save()
        url = f"/api/v1/moments/{moment_image.id}/comments/"
        data = {"content": "评论已删除动态"}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_comment_on_nonexistent_moment(self, auth_client):
        """Test commenting on non-existent moment fails."""
        url = "/api/v1/moments/99999/comments/"
        data = {"content": "评论不存在的动态"}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCommentModel:
    """Tests for Comment model."""

    def test_comment_str(self, moment_image, db):
        """Test Comment __str__ method."""
        from interactions.models import Comment
        comment = Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="测试评论",
        )
        result = str(comment)
        assert str(moment_image.id) in result or str(moment_image.author) in result


@pytest.mark.django_db
class TestCommentSerializer:
    """Tests for Comment serializer."""

    def test_replies_excludes_deleted(self, moment_image, db):
        """Test replies field excludes deleted comments."""
        from interactions.models import Comment
        from interactions.serializers import CommentSerializer

        parent = Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="父评论",
        )
        visible_reply = Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="可见回复",
            parent=parent,
        )
        deleted_reply = Comment.objects.create(
            moment=moment_image,
            author=moment_image.author,
            content="已删除回复",
            parent=parent,
            is_deleted=True,
        )

        serializer = CommentSerializer(parent)
        reply_ids = [r["id"] for r in serializer.data["replies"]]
        assert visible_reply.id in reply_ids
        assert deleted_reply.id not in reply_ids
