from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from apps.adoption.models import AdoptionRequest
from .models import Message
from apps.notifications.models import Notification
from django.contrib import messages

# 1. Unified Inbox View
@login_required
def inbox(request):
    """
    Shows a list of all adoption applications the user is involved in, 
    either as the Adopter or the Donor (the owner of the dog).
    """
    # Find applications where user is the adopter OR the donor of the dog
    # .distinct() ensures we don't see the same chat twice
    applications = AdoptionRequest.objects.filter(
        Q(adopter=request.user) | Q(dog__donor=request.user)
    ).distinct().order_by('-created_at')

    return render(request, 'chat/inbox.html', {
        'applications': applications
    })

# 2. Secure Chat Room View
@login_required
def chat_room(request, application_id):
    """
    Handles the messaging interface for a specific adoption application.
    """
    # Fetch the adoption application
    application = get_object_or_404(AdoptionRequest, id=application_id)
    
    # SECURITY CHECK: Only the Donor (owner) or the Applicant (adopter) can enter
    if request.user != application.adopter and request.user != application.dog.donor:
        messages.error(request, "Access denied. You are not part of this application.")
        return redirect('core:home')

    # POST Logic: Sending a message
    if request.method == 'POST':
        content = request.POST.get('content') 
        if content:
            # A. Save the message to the database
            Message.objects.create(
                application=application,
                sender=request.user,
                text=content
            )

            # B. Identify the receiver to send them a notification
            if request.user == application.adopter:
                receiver = application.dog.donor
            else:
                receiver = application.adopter

            # C. Create a clickable notification for the receiver
            Notification.objects.create(
                recipient=receiver,
                text=f"💬 {request.user.username} sent you a message about {application.dog.name}",
                link=f"/chat/room/{application.id}/" # Matches the URL structure
            )

            return redirect('chat:chat_room', application_id=application.id)

    # Fetch message history
    chat_messages = Message.objects.filter(application=application).order_by('created_at')
    
    # UI Helper: Determine the name of the person you are chatting with
    if request.user == application.adopter:
        chat_partner = application.dog.donor.username
    else:
        # If user is donor, show the adopter's name (from the application field)
        chat_partner = application.full_name

    return render(request, 'chat/chat_room.html', {
        'application': application,
        'dog': application.dog,
        'chat_messages': chat_messages,
        'chat_partner': chat_partner
    })