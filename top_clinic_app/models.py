from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

SPECIALTY_CHOICES = [
    ('general_medicine', 'General Medicine'),
    ('pediatrics', 'Pediatrics'),
    ('cardiology', 'Cardiology'),
    ('dermatology', 'Dermatology'),
    ('orthopedics', 'Orthopedics'),
    ('gynecology_and_obstetrics', 'Gynecology & Obstetrics'),
    ('neurology', 'Neurology'),
    ('psychiatry_and_mental_health', 'Psychiatry & Mental Health'),
]

class Appointment(models.Model):
    specialty = models.CharField(max_length=100, choices=SPECIALTY_CHOICES)
    doctor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_appointments'
    )
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='patient_appointments'
    )
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        unique_together = ('date', 'time', 'specialty', 'doctor')