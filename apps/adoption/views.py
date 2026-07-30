from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from apps.dogs.models import Dog
from apps.notifications.models import Notification
from .models import AdoptionRequest, FinalAdoption

# 1. THE ADOPTION APPLICATION (For Adopters to apply)
@login_required
def apply_adoption(request, dog_id):
    dog = get_object_or_404(Dog, id=dog_id)

    # Prevent donor from adopting their own dog
    if dog.donor == request.user:
        messages.error(request, "You cannot adopt a dog that you listed yourself!")
        return redirect('dogs:dog_detail', pk=dog.id)

    # Prevent duplicate applications
    if AdoptionRequest.objects.filter(dog=dog, adopter=request.user).exists():
        messages.warning(request, "You have already applied for this dog.")
        return redirect('core:home')

    if request.method == 'POST':
        try:
            AdoptionRequest.objects.create(
                dog=dog,
                adopter=request.user,
                full_name=request.user.get_full_name() or request.user.username,
                phone_number=request.user.phone_number,
                city=request.user.city,
                age=request.POST.get('age'),
                family_members=request.POST.get('family_members'),
                house_type=request.POST.get('house_type'),
                reason_for_adoption=request.POST.get('reason'),
                government_id=request.FILES.get('gov_id'),
                occupation="Not Specified",
                monthly_income="0",
                experience_with_pets="N/A",
                address="N/A",
                state="N/A",
                pin_code="000000"
            )

            # Notification to Donor
            Notification.objects.create(
                recipient=dog.donor,
                text=f"🐶 New adoption request for {dog.name} from {request.user.username}!",
                link="/adoption/manage-requests/"
            )

            messages.success(request, f"Application for {dog.name} sent successfully!")
            return redirect('core:home')
        except Exception as e:
            messages.error(request, "Please fill all fields and upload your ID.")

    return render(request, 'adoption/apply_form.html', {'dog': dog})


# 2. DONOR ASSESSMENT VIEW (The Dashboard shown in your screenshot)
@login_required
def donor_applications(request):
    # Only Donors should access this management page
    if request.user.role != 'DONOR':
        messages.error(request, "Access denied. Only Donors can manage adoption requests.")
        return redirect('core:home')

    # Get all applications for dogs owned by this donor
    applications = AdoptionRequest.objects.filter(dog__donor=request.user).order_by('-created_at')
    
    return render(request, 'adoption/donor_applications.html', {
        'applications': applications
    })


# 3. APPROVAL LOGIC
@login_required
def approve_adoption(request, pk):
    if request.method == 'POST':
        # Ensure only the dog's donor can approve the request
        adoption_req = get_object_or_404(AdoptionRequest, pk=pk, dog__donor=request.user)

        if adoption_req.status == 'Approved':
            messages.info(request, "This request has already been approved.")
            return redirect('adoption:manage_applications')

        dog = adoption_req.dog

        # Update Request Status
        adoption_req.status = 'Approved'
        adoption_req.approved_by = request.user
        adoption_req.decision_date = timezone.now()
        adoption_req.save()

        # Update Dog status
        dog.is_available = False
        dog.save()

        # Create Official Record
        FinalAdoption.objects.get_or_create(
            dog=dog, 
            adopter=adoption_req.adopter, 
            processed_by=request.user
        )

        # Notify the Adopter
        Notification.objects.create(
            recipient=adoption_req.adopter,
            text=f"🎉 Congratulations! Your adoption request for {dog.name} has been APPROVED.",
            link="/adoption/my-requests/"
        )

        messages.success(request, f"Adoption Approved: {dog.name} has found a home!")
        return redirect('adoption:manage_applications')


# 4. REJECTION LOGIC
@login_required
def reject_adoption(request, pk):
    if request.method == 'POST':
        adoption_req = get_object_or_404(AdoptionRequest, pk=pk, dog__donor=request.user)

        if adoption_req.status == 'Rejected':
            messages.info(request, "This request has already been rejected.")
            return redirect('adoption:manage_applications')

        reason = request.POST.get('reason')
        if reason == "Other":
            reason = request.POST.get('other_details', 'Not specified')
        
        adoption_req.status = 'Rejected'
        adoption_req.rejection_reason = reason
        adoption_req.decision_date = timezone.now()
        adoption_req.save()

        # Notify the adopter
        Notification.objects.create(
            recipient=adoption_req.adopter,
            text=f"📢 Update: Your request for {adoption_req.dog.name} was REJECTED. Reason: {reason}",
            link="/adoption/my-requests/"
        )

        messages.error(request, f"Request for {adoption_req.dog.name} rejected.")
        return redirect('adoption:manage_applications')


# 5. NEW: DELETE APPLICATION LOGIC (This makes the button work)
@login_required
def delete_application(request, pk):
    """Allows a Donor to delete an application record from their list."""
    application = get_object_or_404(AdoptionRequest, pk=pk)
    
    # Security: Only the Donor who listed the dog can remove this record
    if request.user == application.dog.donor:
        application.delete()
        messages.success(request, "Application record removed successfully.")
    else:
        messages.error(request, "You do not have permission to delete this record.")
        
    return redirect('adoption:manage_applications')


# 6. DASHBOARDS & DETAILS
@login_required
def adoption_request_detail(request, pk):
    req = get_object_or_404(AdoptionRequest, pk=pk)
    
    # Security: Only the donor or a staff member can view application details
    if request.user != req.dog.donor and not request.user.is_staff:
        messages.error(request, "Access denied.")
        return redirect('core:home')
        
    return render(request, 'adoption/request_detail.html', {'req': req})

@login_required
def user_dashboard(request):
    """General dashboard for all users to see their activity"""
    incoming_requests = AdoptionRequest.objects.filter(dog__donor=request.user).order_by('-created_at')
    my_applications = AdoptionRequest.objects.filter(adopter=request.user).order_by('-created_at')
    
    return render(request, 'adoption/dashboard.html', {
        'incoming_requests': incoming_requests,
        'my_applications': my_applications
    })

@login_required
def my_requests(request):
    """View for Adopters to see their sent applications"""
    requests = AdoptionRequest.objects.filter(adopter=request.user).order_by('-created_at')
    return render(request, 'adoption/my_requests.html', {'requests': requests})