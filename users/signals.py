from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Profile

@receiver(post_save, sender=User)
def create_profile_and_assign_group(sender, instance, created, **kwargs):
    if created:
        # Create profile with default role
        profile = Profile.objects.create(user=instance, role='patient')

        # Assign user to Patient group
        patient_group, _ = Group.objects.get_or_create(name='Patient')
        instance.groups.add(patient_group)
    else:
        # Ensure user's group always matches their profile role
        try:
            profile = instance.profile
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=instance, role='patient')

        doctor_group, _ = Group.objects.get_or_create(name='Doctor')
        patient_group, _ = Group.objects.get_or_create(name='Patient')

        instance.groups.clear()
        if profile.role == 'doctor':
            instance.groups.add(doctor_group)
        else:
            instance.groups.add(patient_group)