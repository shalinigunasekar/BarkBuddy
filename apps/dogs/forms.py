from django import forms
from .models import Dog

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        # We handle images manually in the HTML and View, so we exclude them here
        exclude = ['donor', 'is_available', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'health_condition': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }