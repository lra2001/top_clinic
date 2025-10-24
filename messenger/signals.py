from django.db.models.signals import post_save
from django.dispatch import receiver
from top_clinic_app.models import Appointment
from .models import Conversation

@receiver(post_save, sender=Appointment)
def create_conversation(sender, instance, created, **kwargs):
    if created:
        conversation = Conversation.objects.create(appointment=instance)
        conversation.participants.add(instance.patient, instance.doctor)