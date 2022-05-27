from django.urls import path
from . import views

urlpatterns = [
    path('available_spots/', views.get_available_spots)
]