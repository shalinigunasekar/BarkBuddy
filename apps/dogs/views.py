from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib import messages
from .models import Dog, DogImage
from .forms import DogForm

# 1. View to list all dogs (Browse Page)
class DogListView(ListView):
    model = Dog
    template_name = 'dogs/dog_list.html'
    context_object_name = 'dogs'
    paginate_by = 9

    def get_queryset(self):
        queryset = Dog.objects.filter(is_available=True)
        query = self.request.GET.get('q')
        location = self.request.GET.get('location')
        gender = self.request.GET.get('gender')

        if query:
            queryset = queryset.filter(name__icontains=query)
        if location:
            queryset = queryset.filter(district__icontains=location)
        if gender:
            queryset = queryset.filter(gender=gender)
        return queryset.order_by('-created_at')

# 2. View to see Dog Details
def dog_detail(request, pk):
    dog = get_object_or_404(Dog, pk=pk)
    return render(request, 'dogs/dog_detail.html', {'dog': dog})

# 3. View to Add a New Dog (Donor only)
@login_required
def add_dog(request):
    # Only registered Donors can add dogs
    if request.user.role != 'DONOR':
        messages.error(request, "Only registered Donors can list dogs.")
        return redirect('core:home')

    if request.method == 'POST':
        # FIX: We pass request.FILES to the form
        form = DogForm(request.POST, request.FILES)
        
        # Get the list of images from the manual HTML input name="images"
        images = request.FILES.getlist('images')
        
        if form.is_valid():
            dog = form.save(commit=False)
            dog.donor = request.user
            dog.save()
            
            # Logic to save each image file to the database
            if images:
                for img in images:
                    DogImage.objects.create(dog=dog, image=img)
                messages.success(request, f"{dog.name} has been published successfully with images!")
            else:
                messages.warning(request, f"{dog.name} published, but no images were uploaded.")
                
            return redirect('core:home')
        else:
            # If form is NOT valid, show error messages on the screen
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
            
            # Also print errors in the terminal for debugging
            print("Form Errors:", form.errors)
    else:
        form = DogForm()
    
    return render(request, 'dogs/dog_form.html', {'form': form})