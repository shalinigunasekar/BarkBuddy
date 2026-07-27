from django.db.models.signals import post_save
from django.dispatch import receiver
import apps.adoption.models
from apps.notifications.models import Notification

class receiver:
    def __init__(self, signal, sender=None, weak=True, dispatch_uid=None):
        self.signal = signal
        self.sender = sender
        self.weak = weak
        self.dispatch_uid = dispatch_uid

    def __call__(self, func):
        self.signal.connect(
            func,
            sender=self.sender,
            weak=self.weak,
            dispatch_uid=self.dispatch_uid,
        )
        return func

    def disconnect(self, func):
        self.signal.disconnect(
            func,
            sender=self.sender,
            weak=self.weak,
            dispatch_uid=self.dispatch_uid,
        )
        return func


@receiver(post_save, sender=apps.adoption.models.AdoptionRequest)
def create_status_notification(sender, instance, created, **kwargs):
    if not created: # If the status was updated
        Notification.objects.create(
            recipient=instance.adopter,
            notification_type='STATUS',
            text=f"Your request for {instance.dog.name} has been {instance.status.lower()}.",
            link=f"/adoption/adopter-dashboard/"
        )