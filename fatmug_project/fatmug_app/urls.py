from django.urls import path
from . import views

# Define other URL patterns here
urlpatterns = [
    path('api/vendors', views.create_and_get_vendor,
         name='create_and_get_vendor'),
    path('api/vendors/<int:vendor_id>', views.update_and_get_single_vendor,
         name='update_and_get_single_vendor'),
]