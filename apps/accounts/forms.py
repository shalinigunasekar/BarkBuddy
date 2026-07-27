from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.Role.choices, widget=forms.RadioSelect, help_text="Choose how you want to use BarkBuddy")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'phone_number', 'city')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'bio', 'city', 'state']