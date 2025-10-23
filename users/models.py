from django.db import models
from django.contrib.auth.models import User, Group
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

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

        # Resize image only if local file exists
        if self.image and hasattr(self.image, 'path'):
            img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        else:
        # For Cloudinary, skip resizing to avoid path errors
            pass