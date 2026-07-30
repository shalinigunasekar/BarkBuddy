from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from .models import Dog, DogImage
from .forms import DogForm

# 1. View to list all dogs
class DogListView(ListView):
    model = Dog
    template_name = 'dogs/dog_list.html'
    context_object_name = 'dogs'
    paginate_by = 9

    def get_queryset(self):
        queryset = Dog.objects.all()
        return queryset.order_by('-created_at')

# 2. View to see Dog Details
def dog_detail(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    return render(request, 'dogs/dog_detail.html', {'dog': dog})

# 3. View to Add a New Dog
@login_required
def add_dog(request):
    if request.user.role != 'DONOR':
        messages.error(request, "Only registered Donors can list dogs.")
        return redirect('core:home')

    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        
        if form.is_valid():
            dog = form.save(commit=False)
            dog.donor = request.user
            dog.save()
            
            if images:
                for img in images:
                    DogImage.objects.create(dog=dog, image=img)
                messages.success(request, f"{dog.name} has been published successfully!")
            else:
                messages.warning(request, f"{dog.name} published without images.")
                
            return redirect('core:home')
    else:
        form = DogForm()
    
    return render(request, 'dogs/dog_form.html', {'form': form})

# 4. View to Edit Dog Details (NEW - Fixing your issue)
@login_required
def edit_dog(request, pk):
    # 1. Fetch the dog or 404
    dog = get_object_or_404(Dog, pk=pk)

    # 2. Security Check: Only the donor who listed the dog can edit it
    if dog.donor != request.user:
        messages.error(request, "You are not authorized to edit this listing.")
        return redirect('dogs:dog_detail', pk=pk)

    # 3. Handle Form Submission
    if request.method == 'POST':
        # Pass 'instance=dog' so it updates the existing record
        form = DogForm(request.POST, request.FILES, instance=dog)
        if form.is_valid():
            form.save()
            messages.success(request, f"Details for {dog.name} updated successfully!")
            return redirect('dogs:dog_detail', pk=dog.pk)
    else:
        # Load the form with existing dog data
        form = DogForm(instance=dog)

    return render(request, 'dogs/dog_form.html', {
        'form': form,
        'dog': dog,
        'edit_mode': True # Used in template to change button text to "Save Changes"
    })

# 5. Direct Delete Logic for Dog Listing
@login_required
def delete_dog(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    
    # Security Check
    if dog.donor == request.user:
        dog_name = dog.name
        dog.delete()
        messages.success(request, f"Listing for {dog_name} has been removed.")
    else:
        messages.error(request, "You do not have permission to delete this.")
    
    return redirect('dogs:dog_list')