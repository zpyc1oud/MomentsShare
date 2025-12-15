import time

from celery import shared_task
from django.db import transaction

from .models import Moment


@shared_task
def transcode_video(moment_id: int):
    try:
        moment = Moment.objects.get(id=moment_id)
    except Moment.DoesNotExist:
        return
    # Simulate processing delay
    time.sleep(1)
    with transaction.atomic():
        moment.video_status = Moment.VideoStatus.READY
        moment.save(update_fields=["video_status"])

