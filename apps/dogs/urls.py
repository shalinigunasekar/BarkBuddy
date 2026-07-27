from django.urls import path
from . import views

app_name = 'dogs' # Nickname for the dogs app

urlpatterns = [
    # The name must be 'dog_list'
    path('', views.DogListView.as_view(), name='dog_list'), 
    path('add/', views.add_dog, name='dog_add'),
    path('<int:pk>/', views.dog_detail, name='dog_detail'),
]