from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        DONOR = "DONOR", "Donor"
        ADOPTER = "ADOPTER", "Adopter"

    role = models.CharField(
        max_length=10, 
        choices=Role.choices, 
        default=Role.ADOPTER
    )
    
    # FIXED: Added unique=True to prevent duplicate mobile numbers
    phone_number = models.CharField(
        max_length=15, 
        unique=True, 
        null=True, 
        blank=True,
        help_text="Enter a unique mobile number"
    )
    
    profile_picture = models.ImageField(upload_to='profiles/', default='profiles/default_user.png', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"