from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        # This count is what appears on the red circle of the bell
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}