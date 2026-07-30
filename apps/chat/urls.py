from django.urls import path
from . import views

# This namespace allows you to use {% url 'chat:inbox' %}
app_name = 'chat'

urlpatterns = [
    # 1. Inbox / Message List 
    # This is the "map" that fixed your 'NoReverseMatch' error
    path('inbox/', views.inbox, name='inbox'),
    
    # 2. Chat Room 
    # Changed from 'chat_view' to 'chat_room' to match the function in views.py
    # Changed <int:user_id> to <int:application_id> to match your logic
    path('room/<int:application_id>/', views.chat_room, name='chat_room'),
]