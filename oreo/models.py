from django.db import models


class Message(models.Model):
    """
    model for messages
    """

    title = models.CharField(max_length=100)
    body = models.TextField()
    send_flag = models.BooleanField(default=False)
    read_flag = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
