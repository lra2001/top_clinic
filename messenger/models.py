from django.db import models
from django.contrib.auth.models import User
from top_clinic_app.models import Appointment
from django.utils import timezone

# Create your models here.

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    appointment = models.ForeignKey(
        'top_clinic_app.Appointment', on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"

class ConversationStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_status')
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='statuses')
    is_archived = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'conversation')