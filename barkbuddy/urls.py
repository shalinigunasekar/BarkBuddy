from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Django Admin Panel
    path('admin/', admin.site.urls),

    # 2. Core App (Home, About, Contact)
    path('', include('apps.core.urls')),

    # 3. Accounts App (Login, Register, Logout, Profile)
    path('accounts/', include('apps.accounts.urls')),

    # 4. Dogs App (Listings, Add Dog, Details)
    path('dogs/', include('apps.dogs.urls')),

    # 5. Adoption App (Applications, Dashboard)
    path('adoption/', include('apps.adoption.urls')),

    # 6. Chat App (Messaging system)
    # This inclusion allows for the 'chat:' namespace
    path('chat/', include('apps.chat.urls')),

    # 7. Notifications App (Bell Icon logic)
    path('notifications/', include('apps.notifications.urls')),
]

# This block allows Django to serve uploaded images and CSS files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)