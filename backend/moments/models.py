from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Moment(models.Model):
    class MomentType(models.TextChoices):
        IMAGE = "IMAGE", "IMAGE"
        VIDEO = "VIDEO", "VIDEO"

    class VideoStatus(models.TextChoices):
        PROCESSING = "PROCESSING", "PROCESSING"
        READY = "READY", "READY"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="moments")
    content = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=MomentType.choices)
    video_file = models.FileField(upload_to="videos/", blank=True, null=True)
    video_status = models.CharField(
        max_length=15, choices=VideoStatus.choices, default=VideoStatus.READY
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, through="MomentTag", blank=True, related_name="moments")

    def __str__(self):
        return f"{self.author} - {self.type} - {self.created_at}"


class MomentTag(models.Model):
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("moment", "tag")


class Image(models.Model):
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name="images")
    image_file = models.ImageField(upload_to="images/")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Image {self.order} for moment {self.moment_id}"

