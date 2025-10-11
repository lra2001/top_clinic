# top_clinic_app/admin.py
from django.contrib import admin
from .models import Appointment

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('specialty', 'doctor', 'patient', 'date', 'time', 'created_at')
    list_filter = ('specialty', 'date', 'doctor')
    search_fields = ('patient__username', 'doctor__username')
