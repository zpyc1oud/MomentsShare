"""
Tests for Celery tasks - covers all branches.
"""
import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.django_db
class TestTranscodeVideoTask:
    """Tests for transcode_video task (C-05)."""

    def test_transcode_video_success(self, moment_video_processing):
        """Test successful video transcoding."""
        from moments.tasks import transcode_video
        from moments.models import Moment

        # Run the task
        transcode_video(moment_video_processing.id)

        # Verify status updated
        moment_video_processing.refresh_from_db()
        assert moment_video_processing.video_status == Moment.VideoStatus.READY

    def test_transcode_video_nonexistent_moment(self, db):
        """Test transcoding non-existent moment."""
        from moments.tasks import transcode_video

        # Should not raise exception
        result = transcode_video(99999)
        # Task should handle gracefully

    def test_transcode_video_already_ready(self, moment_video):
        """Test transcoding already ready video."""
        from moments.tasks import transcode_video
        from moments.models import Moment

        # Already READY
        assert moment_video.video_status == Moment.VideoStatus.READY

        # Run task - should complete without error
        transcode_video(moment_video.id)

        moment_video.refresh_from_db()
        assert moment_video.video_status == Moment.VideoStatus.READY

