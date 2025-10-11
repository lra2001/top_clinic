from django.db import models
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100, choices=SPECIALTY_CHOICES)
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ('date', 'time', 'specialty')