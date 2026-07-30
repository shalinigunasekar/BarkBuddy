from django.urls import path
from . import views

app_name = 'dogs'

urlpatterns = [
    path('', views.DogListView.as_view(), name='dog_list'), 
    path('add/', views.add_dog, name='add_dog'),
    path('<int:pk>/', views.dog_detail, name='dog_detail'),
    path('<int:pk>/delete/', views.delete_dog, name='delete_dog'),
    
    # ADD THIS LINE:
    path('<int:pk>/edit/', views.edit_dog, name='edit_dog'),
]