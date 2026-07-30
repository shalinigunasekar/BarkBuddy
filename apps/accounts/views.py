from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Internal Imports
from .forms import CustomUserCreationForm, UserUpdateForm 
from apps.dogs.models import Dog 

# Initialize the correct User model (the custom one defined in settings)
User = get_user_model()

# 1. Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to BarkBuddy, {user.username}!")
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# 2. Private Profile View (Edit own settings)
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

# 3. PUBLIC Donor Profile View (What Adopters see)
# FIXED: Now uses the correct Custom User model reference
def user_profile(request, pk):
    # Fetch the donor's details using the correct table
    profile_user = get_object_or_404(User, pk=pk)
    
    # Fetch all dogs listed by this specific donor
    donor_dogs = Dog.objects.filter(donor=profile_user)
    
    return render(request, 'accounts/donor_profile.html', {
        'profile_user': profile_user,
        'donor_dogs': donor_dogs
    })

# 4. Logout View
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')