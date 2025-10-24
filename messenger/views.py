from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Conversation, Message
from top_clinic_app.models import Appointment
from .forms import MessageForm

# Create your views here.

@login_required
def inbox(request):
    if hasattr(request.user, 'profile') and request.user.profile.role == 'patient':
        appointments = Appointment.objects.filter(patient=request.user)
    elif hasattr(request.user, 'profile') and request.user.profile.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.none()

    conversations = Conversation.objects.filter(appointment__in=appointments)

    # Add unread count to each conversation
    for conv in conversations:
        conv.unread_count = conv.messages.filter(is_read=False).exclude(sender=request.user).count()

    # Total unread for navbar badge
    total_unread = sum(conv.unread_count for conv in conversations)

    return render(request, 'messenger/inbox.html', {
        'conversations': conversations,
        'total_unread': total_unread
    })


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages_qs = conversation.messages.all().order_by('created_at')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user

            # Determine recipient: the other participant in the appointment
            if request.user == conversation.appointment.patient:
                msg.recipient = conversation.appointment.doctor
            else:
                msg.recipient = conversation.appointment.patient

            msg.save()
            messages.success(request, 'Message sent!')
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()

    # Mark messages as read if they are from the other participant
    for msg in messages_qs.filter(is_read=False).exclude(sender=request.user):
        msg.is_read = True
        msg.save()

    return render(request, 'messenger/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages_qs,
        'form': form
    })


@login_required
def start_conversation(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check if conversation already exists
    conversation = Conversation.objects.filter(appointment=appointment).first()
    if not conversation:
        conversation = Conversation.objects.create(appointment=appointment)

    return redirect('conversation_detail', conversation.id)

@login_required
def archive_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Optional: only participants can archive
    participants = [conversation.appointment.patient, conversation.appointment.doctor]
    if request.user not in participants:
        messages.error(request, "You are not allowed to archive this conversation.")
        return redirect('inbox')

    conversation.is_archived = True
    conversation.save()
    messages.success(request, "Conversation archived successfully.")
    return redirect('inbox')