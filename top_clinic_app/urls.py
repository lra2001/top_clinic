from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('specialties/', views.specialties, name='specialties'),
    path('contact/', views.contact, name='contact'),
    path('appointments/', views.appointments, name='appointments'),
    path('get-slots/', views.get_available_slots, name='get_slots'),
]