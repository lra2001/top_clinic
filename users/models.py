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

        if self.image:
            try:
                img = Image.open(self.image.file)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)

                    # Save the resized image back to the storage
                    buffer = BytesIO()
                    img.save(buffer, format=img.format)
                    buffer.seek(0)
                    self.image.save(self.image.name, ContentFile(buffer.read()), save=False)
            except Exception as e:
                # Log or handle the exception if needed
                print(f"Error resizing image: {e}")