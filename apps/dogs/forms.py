import re
from django import forms
from django.core.exceptions import ValidationError
from geopy.geocoders import Nominatim  # Free geocoding service
from .models import Dog

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        exclude = ['donor', 'is_available', 'created_at', 'updated_at']
        # ... your existing widgets ...

    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get('location')
        district = cleaned_data.get('district')
        state = cleaned_data.get('state')

        # Only validate if all three fields are provided
        if location and district and state:
            # 1. Create a search string
            search_query = f"{location}, {district}, {state}, India"
            
            # 2. Use Geopy to check if this place exists
            try:
                # 'user_agent' should be your project name
                geolocator = Nominatim(user_agent="barkbuddy_app")
                # timeout=10 allows time for the map service to respond
                possible_address = geolocator.geocode(search_query, timeout=10)

                if not possible_address:
                    # If the map service finds nothing, it's an invalid location
                    raise ValidationError({
                        'location': "We couldn't find this location on the map. Please enter a valid street or landmark name.",
                        'district': "Ensure the district name is correct.",
                    })
                
                # Optional: Print the real found address in terminal for debugging
                print(f"--- VALID LOCATION FOUND: {possible_address.address} ---")

            except (ValidationError, Exception) as e:
                # If there's a network error or map error, we allow it (don't block the user)
                # but if it's a ValidationError, we re-raise it.
                if isinstance(e, ValidationError):
                    raise e
                print(f"Geocoding Error: {e}")

        return cleaned_data

    # Keep your specific "abcd" regex checks for individual fields as well
    def clean_district(self):
        data = self.cleaned_data.get('district', '').strip()
        if not re.match(r'^[a-zA-Z\s]+$', data) or data.lower() in ['abcd', 'asdf']:
            raise ValidationError("Please enter a valid district name.")
        return data.title()