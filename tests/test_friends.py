"""
Tests for friends module - covers all branches.
"""
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestFriendRequest:
    """Tests for friend request (S-01-a)."""

    def test_friend_request_success(self, auth_client, user, user2):
        """Test sending friend request successfully."""
        url = "/api/v1/friends/request/"
        data = {"to_user_id": user2.id}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "PENDING"

    def test_friend_request_to_self_fails(self, auth_client, user):
        """Test sending friend request to self fails."""
        url = "/api/v1/friends/request/"
        data = {"to_user_id": user.id}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_friend_request_duplicate_fails(self, auth_client, user, user2, friendship_pending):
        """Test duplicate friend request fails."""
        url = "/api/v1/friends/request/"
        data = {"to_user_id": user2.id}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_friend_request_missing_to_user_id(self, auth_client):
        """Test friend request without to_user_id fails."""
        url = "/api/v1/friends/request/"
        response = auth_client.post(url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestFriendRespond:
    """Tests for responding to friend request (S-01-b, S-01-c)."""

    def test_accept_friend_request(self, auth_client2, user, user2, friendship_pending):
        """Test accepting friend request."""
        url = "/api/v1/friends/respond/"
        data = {
            "request_id": friendship_pending.id,
            "action": "accept",
        }
        response = auth_client2.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "ACCEPTED"

    def test_reject_friend_request(self, auth_client2, user, user2, friendship_pending):
        """Test rejecting friend request."""
        url = "/api/v1/friends/respond/"
        data = {
            "request_id": friendship_pending.id,
            "action": "reject",
        }
        response = auth_client2.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "REJECTED"

    def test_respond_invalid_action(self, auth_client2, user, user2, friendship_pending):
        """Test responding with invalid action fails."""
        url = "/api/v1/friends/respond/"
        data = {
            "request_id": friendship_pending.id,
            "action": "invalid",
        }
        response = auth_client2.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_respond_missing_params(self, auth_client2):
        """Test responding without required params fails."""
        url = "/api/v1/friends/respond/"
        response = auth_client2.post(url, {})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_respond_nonexistent_request(self, auth_client2):
        """Test responding to non-existent request fails."""
        url = "/api/v1/friends/respond/"
        data = {
            "request_id": 99999,
            "action": "accept",
        }
        response = auth_client2.post(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_respond_by_wrong_user(self, auth_client, user, user2, friendship_pending):
        """Test responding by sender (not receiver) fails."""
        # auth_client is user (sender), should not be able to respond
        url = "/api/v1/friends/respond/"
        data = {
            "request_id": friendship_pending.id,
            "action": "accept",
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestFriendDelete:
    """Tests for deleting friend (S-01-d)."""

    def test_delete_friend_success(self, auth_client, user, user2, friendship_accepted):
        """Test deleting friend successfully (physical delete)."""
        url = f"/api/v1/friends/{user2.id}/"
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify physical delete
        from friends.models import Friendship
        assert not Friendship.objects.filter(id=friendship_accepted.id).exists()

    def test_delete_friend_by_receiver(self, auth_client2, user, user2, friendship_accepted):
        """Test receiver can also delete friendship."""
        url = f"/api/v1/friends/{user.id}/"
        response = auth_client2.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_nonexistent_friendship(self, auth_client, user2):
        """Test deleting non-existent friendship fails."""
        url = f"/api/v1/friends/{user2.id}/"
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestFriendshipModel:
    """Tests for Friendship model."""

    def test_friendship_str(self, friendship_accepted):
        """Test Friendship __str__ method."""
        result = str(friendship_accepted)
        assert "ACCEPTED" in result

