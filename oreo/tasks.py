from celery import shared_task

from .models import Message


@shared_task
def update_send_flag(data, pk):
    """
    celery task to set send_flag in true
    """

    status: int = 200  # simulate reading status
    if status == 200:
        message = Message.objects.get(pk=pk)
        message.send_flag = True
        message.save()
