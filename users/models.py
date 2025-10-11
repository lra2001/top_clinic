from django.db import models
from django.contrib.auth.models import User, Group
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    SPECIALTIES = [
        ('general_medicine', 'General Medicine'),
        ('pediatrics', 'Pediatrics'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('orthopedics', 'Orthopedics'),
        ('gynecology_and_obstetrics', 'Gynecology & Obstetrics'),
        ('neurology', 'Neurology'),
        ('psychiatry_and_mental_health', 'Psychiatry & Mental Health'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    specialty = models.CharField(max_length=50, choices=SPECIALTIES, blank=True, null=True)
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        # If the user is created via registration (not admin), default to patient
        patient_group, _ = Group.objects.get_or_create(name='Patient')
        instance.groups.add(patient_group)
        profile.role = 'patient'
        profile.save()

@receiver(post_save, sender=Profile)
def assign_user_group(sender, instance, **kwargs):
    doctor_group, _ = Group.objects.get_or_create(name='Doctor')
    patient_group, _ = Group.objects.get_or_create(name='Patient')

    # Clear previous groups to prevent duplicates
    instance.user.groups.clear()

    if instance.role == 'doctor':
        instance.user.groups.add(doctor_group)
    else:
        instance.user.groups.add(patient_group)