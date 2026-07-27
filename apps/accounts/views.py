from django.shortcuts import render, redirect
from django.contrib.auth import login, logout  # <--- logout MUST be here
from django.contrib.auth.decorators import login_required
# Import the form names exactly as they are in your forms.py
from .forms import CustomUserCreationForm, UserUpdateForm 
from django.contrib import messages

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

# 2. Profile View
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

# 3. Logout View (Fixed)
def user_logout(request):
    logout(request) # Now Python knows what this is!
    messages.info(request, "You have been logged out.")
    return redirect('core:home')