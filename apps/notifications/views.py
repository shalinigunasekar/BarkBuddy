from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_center(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'notifications/center.html', {'notifications': notifications})

@login_required
def read_and_redirect(request, n_id):
    # Fetch the notification
    notification = get_object_or_404(Notification, id=n_id, recipient=request.user)
    
    # 1. Mark as read (Clears the bell icon number)
    notification.is_read = True
    notification.save()
    
    # 2. Redirect to the source (e.g., the Chat Room link)
    if notification.link:
        return redirect(notification.link)
    
    return redirect('notifications:list')

@login_required
def delete_notification(request, n_id):
    notification = get_object_or_404(Notification, id=n_id, recipient=request.user)
    notification.delete()
    return redirect('notifications:list')