from django.contrib import admin
from .models import Dog, DogImage

class DogImageInline(admin.TabularInline):
    model = DogImage
    extra = 3 # Allows you to upload 3 images at once in admin

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'gender', 'age', 'district', 'is_available')
    list_filter = ('gender', 'age', 'vaccinated', 'is_available')
    search_fields = ('name', 'breed', 'district')
    inlines = [DogImageInline]