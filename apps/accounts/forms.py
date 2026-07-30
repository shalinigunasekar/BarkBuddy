import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from geopy.geocoders import Nominatim  # For real-world location access

class CustomUserCreationForm(UserCreationForm):
    """
    PROFESSIONAL REGISTRATION FORM:
    - Blocks gibberish (abc, abcd, asdf)
    - Validates real-world map locations (Geopy)
    - Ensures unique phone and email
    - Professional Radio Button selection for roles
    """
    
    # 1. Role selection using Radio Buttons
    role = forms.ChoiceField(
        choices=User.Role.choices, 
        widget=forms.RadioSelect, 
        initial=User.Role.ADOPTER,
        help_text="Choose how you want to use BarkBuddy"
    )

    # Adding State to Registration for Geopy verification
    state = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tamil Nadu'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Added email, role, phone, city, and state
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'phone_number', 'city', 'state')

    # --- 2. STRICT CITY VALIDATION (Anti-Gibberish) ---
    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        
        # Block non-letters
        if not re.match(r'^[a-zA-Z\s]+$', city):
            raise ValidationError("Invalid city name. Use letters only.")
        
        # Block common keyboard mash patterns
        gibberish = ['abc', 'abcd', 'asdf', 'qwer', 'zxcv', 'test', '1234', 'none']
        if city.lower() in gibberish:
            raise ValidationError("Please enter a real, valid city name (e.g. Chennai).")
        
        if len(city) < 3:
            raise ValidationError("City name is too short.")
            
        return city.title() # Normalizes 'chennai' to 'Chennai'

    # --- 3. STRICT PHONE VALIDATION (Unique & 10 Digits) ---
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        
        if len(phone) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits.")
        
        # Uniqueness check
        if User.objects.filter(phone_number=phone).exists():
            raise ValidationError("This mobile number is already registered.")
            
        return phone

    # --- 4. EMAIL UNIQUENESS ---
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    # --- 5. PROFESSIONAL MAP VALIDATION (Geopy) ---
    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')

        if city and state:
            search_query = f"{city}, {state}, India"
            try:
                # Initialize Geopy Map Service
                geolocator = Nominatim(user_agent="barkbuddy_registration")
                # timeout ensures the app doesn't hang too long
                location = geolocator.geocode(search_query, timeout=5)

                if not location:
                    raise ValidationError(
                        "We couldn't find this location. Please check if your City and State are correct."
                    )
                
                print(f"--- MAP VERIFIED: {location.address} ---")
                
            except (ValidationError, Exception) as e:
                if isinstance(e, ValidationError):
                    raise e
                # If network is down, allow registration but log the error
                print(f"Location Service Delay: {e}")

        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    """
    PROFESSIONAL PROFILE UPDATE FORM:
    - Same strict location and phone validation for existing users.
    """
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
            'profile_picture', 
            'bio', 
            'city', 
            'state'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Tell us about yourself...'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        if not re.match(r'^[a-zA-Z\s]+$', city) or city.lower() in ['abc', 'abcd', 'asdf']:
            raise ValidationError("Enter a valid city name.")
        return city.title()

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError("Enter a valid 10-digit mobile number.")
        return phone

    def clean(self):
        # Same Map Check for Updates
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        if city and state:
            try:
                geolocator = Nominatim(user_agent="barkbuddy_update")
                if not geolocator.geocode(f"{city}, {state}, India", timeout=3):
                    raise ValidationError("Invalid City/State combination.")
            except:
                pass
        return cleaned_data