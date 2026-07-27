from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.dogs.models import Dog
from apps.notifications.models import Notification  # Crucial for the Bell Icon
from .models import AdoptionRequest
from django.contrib import messages

# 1. View for Adopters to fill out the application form
@login_required
def apply_adoption(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    
    # Security: Only Adopters can apply
    if request.user.role != 'ADOPTER':
        messages.error(request, "Only registered Adopters can apply. You are logged in as a Donor.")
        return redirect('dogs:dog_detail', pk=dog.id)

    # Prevent duplicate applications
    if AdoptionRequest.objects.filter(dog=dog, adopter=request.user).exists():
        messages.warning(request, "You have already applied for this dog.")
        return redirect('core:home')

    if request.method == 'POST':
        try:
            # Capturing all model fields to prevent IntegrityError (like family_members)
            AdoptionRequest.objects.create(
                dog=dog,
                adopter=request.user,
                full_name=request.POST.get('full_name'),
                age=request.POST.get('age', 0),
                occupation=request.POST.get('occupation', 'Not Specified'),
                monthly_income=request.POST.get('income', 'Not Specified'),
                experience_with_pets=request.POST.get('experience', 'None'),
                house_type=request.POST.get('house_type', 'Other'),
                family_members=request.POST.get('family_members', 1), 
                reason_for_adoption=request.POST.get('reason'),
                phone_number=request.POST.get('phone'),
                email=request.user.email,
                address=request.POST.get('address', 'Not Provided'),
                city=request.POST.get('city', 'Not Provided'),
                state=request.POST.get('state', 'Not Provided'),
                pin_code=request.POST.get('pincode', '000000'),
                government_id=request.FILES.get('gov_id')
            )
            messages.success(request, f"Success! Your application for {dog.name} has been submitted.")
            return redirect('core:home')
        except Exception as e:
            messages.error(request, f"Error saving request: {e}")

    return render(request, 'adoption/apply_form.html', {'dog': dog})

# 2. View for Adopters to see their own sent applications
@login_required
def my_requests(request):
    if request.user.role != 'ADOPTER':
        return redirect('core:home')
    requests = AdoptionRequest.objects.filter(adopter=request.user).order_by('-created_at')
    return render(request, 'adoption/my_requests.html', {'requests': requests})

# 3. View for Donors to see incoming requests on their Dashboard
@login_required
def donor_dashboard(request):
    if request.user.role != 'DONOR':
        return redirect('core:home')
    my_dogs = Dog.objects.filter(donor=request.user)
    incoming_requests = AdoptionRequest.objects.filter(dog__donor=request.user).order_by('-created_at')
    return render(request, 'adoption/donor_dashboard.html', {
        'my_dogs': my_dogs,
        'incoming_requests': incoming_requests
    })

# 4. View to Accept or Reject an adoption (THE STATUS UPDATER)
@login_required
def update_request_status(request, req_id, status):
    # Security: Ensure only the dog's Donor can change the status
    adoption_req = get_object_or_404(AdoptionRequest, id=req_id, dog__donor=request.user)
    dog = adoption_req.dog
    
    if status == 'Accepted':
        adoption_req.status = 'Accepted'
        
        # Logic: Mark the dog as Adopted (unavailable) so it leaves the marketplace
        dog.is_available = False
        dog.save()

        # Notification: Create a message for the Adopter (Triggering Bell Icon)
        Notification.objects.create(
            recipient=adoption_req.adopter,
            text=f"Congratulations! Your adoption request for {dog.name} has been APPROVED."
        )
        messages.success(request, f"You have accepted the request for {dog.name}. The dog is now marked as Adopted.")

    elif status == 'Rejected':
        adoption_req.status = 'Rejected'
        
        # Notification: Notify the Adopter of the rejection
        Notification.objects.create(
            recipient=adoption_req.adopter,
            text=f"Update: The donor has declined your request for {dog.name}."
        )
        messages.warning(request, "Adoption request has been rejected.")
    
    adoption_req.save()
    return redirect('adoption:donor_dashboard')