from django.conf import settings
from django.db import models
from django.utils import timezone

from moments.models import Moment

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    created_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return f"{self.author} on {self.moment_id}"


class Like(models.Model):
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("moment", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} likes {self.moment}"


class Rating(models.Model):
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField(default=5)  # 1-5
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("moment", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} rated {self.moment} - {self.score}"


class Message(models.Model):
    """私信消息模型"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"