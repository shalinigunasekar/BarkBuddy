from django.db import models  # <--- THIS WAS THE MISSING LINE
from django.conf import settings

class Dog(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    AGE_CHOICES = [
        ('Puppy', 'Puppy'), 
        ('Young', 'Young'), 
        ('Adult', 'Adult'), 
        ('Senior', 'Senior')
    ]

    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donated_dogs')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, default="Indie / Unknown")
    age = models.CharField(max_length=20, choices=AGE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    vaccinated = models.BooleanField(default=False)
    sterilized = models.BooleanField(default=False)
    health_condition = models.TextField(blank=True)
    
    friendly_with_kids = models.BooleanField(default=True)
    friendly_with_dogs = models.BooleanField(default=True)
    friendly_with_cats = models.BooleanField(default=False)
    
    description = models.TextField()
    
    location = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    
    contact_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField()

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.breed})"

class DogImage(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='dog_gallery/')

    def __str__(self):
        return f"Image for {self.dog.name}"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='favored_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'dog')

    def __str__(self):
        return f"{self.user.username} liked {self.dog.name}"