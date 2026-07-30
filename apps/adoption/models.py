from django.db import models
from django.conf import settings
from apps.dogs.models import Dog

class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Adoption Completed'),
    ]

    HOUSE_TYPE_CHOICES = [
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Bungalow', 'Bungalow'),
        ('Other', 'Other'),
    ]

    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='adoption_requests')
    # FIXED LINE BELOW: Changed on_backend_models to on_delete
    adopter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_requests')
    
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    occupation = models.CharField(max_length=100)
    monthly_income = models.CharField(max_length=50)
    experience_with_pets = models.TextField(help_text="Describe your previous experience with pets")
    house_type = models.CharField(max_length=20, choices=HOUSE_TYPE_CHOICES)
    is_rental = models.BooleanField(default=False, verbose_name="Is it a rental property?")
    family_members = models.PositiveIntegerField(help_text="Number of people in household")
    reason_for_adoption = models.TextField()
    
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    
    government_id = models.ImageField(upload_to='id_proofs/', help_text="Upload Govt ID (Aadhar/Voter ID)")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    rejection_reason = models.CharField(max_length=100, blank=True, null=True)
    rejection_details = models.TextField(blank=True, null=True)
    
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='processed_requests'
    )
    decision_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.dog.name} by {self.full_name}"

class FinalAdoption(models.Model):
    dog = models.OneToOneField(Dog, on_delete=models.CASCADE)
    adopter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    adoption_date = models.DateTimeField(auto_now_add=True)
    # FIXED LINE BELOW: Changed on_backend_models to on_delete
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='adoptions_witnessed')
    
    def __str__(self):
        return f"OFFICIAL: {self.dog.name} adopted by {self.adopter.username}"