from django.db import models
from django.conf import settings
from apps.adoption.models import AdoptionRequest

class Message(models.Model):
    application = models.ForeignKey(AdoptionRequest, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"From {self.sender.username} at {self.created_at}"