from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AdoptionRequest
from apps.notifications.models import Notification

@receiver(post_save, sender=AdoptionRequest)
def adoption_notification_signal(sender, instance, created, **kwargs):
    # 1. If a new request is created, notify the Donor
    if created:
        Notification.objects.create(
            recipient=instance.dog.donor,
            text=f"🔔 New adoption request for {instance.dog.name} from {instance.full_name}!",
            link="/adoption/dashboard/"
        )
    
    # 2. If the status was UPDATED, notify the Adopter
    else:
        if instance.status == 'Accepted':
            # Create ONLY the Accepted message
            Notification.objects.create(
                recipient=instance.adopter,
                text=f"🎉 Congratulations! Your request for {instance.dog.name} has been APPROVED.",
                link="/adoption/my-requests/"
            )
        elif instance.status == 'Rejected':
            # Create ONLY the Rejected message
            Notification.objects.create(
                recipient=instance.adopter,
                text=f"❌ Update: Your request for {instance.dog.name} was not accepted.",
                link="/adoption/my-requests/"
            )