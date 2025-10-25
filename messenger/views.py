from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Conversation, Message, ConversationStatus
from top_clinic_app.models import Appointment
from .forms import MessageForm

# Create your views here.

@login_required
def inbox(request):
    if request.user.profile.role == 'patient':
        appointments = Appointment.objects.filter(patient=request.user)
    elif request.user.profile.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user)
    else:
        appointments = Appointment.objects.none()

    all_conversations = Conversation.objects.filter(appointment__in=appointments)
    active_conversations = []
    archived_conversations = []

    for conv in all_conversations:
        conv.unread_count = conv.messages.filter(is_read=False).exclude(sender=request.user).count()
        status = conv.statuses.filter(user=request.user).first()
        if status and status.is_archived:
            archived_conversations.append(conv)
        else:
            active_conversations.append(conv)

    total_unread = sum(conv.unread_count for conv in active_conversations)

    return render(request, 'messenger/inbox.html', {
        'active_conversations': active_conversations,
        'archived_conversations': archived_conversations,
        'total_unread': total_unread,
    })


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    chat_messages = conversation.messages.all().order_by('created_at')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user

            # Determine recipient
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
    for msg in chat_messages.filter(is_read=False).exclude(sender=request.user):
        msg.is_read = True
        msg.save()

    return render(request, 'messenger/conversation_detail.html', {
        'conversation': conversation,
        'chat_messages': chat_messages,
        'form': form,
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
    status, created = ConversationStatus.objects.get_or_create(
        user=request.user, conversation=conversation
    )
    status.is_archived = True
    status.save()
    messages.success(request, 'Conversation archived.')
    return redirect('inbox')

@login_required
def unarchive_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    status, created = ConversationStatus.objects.get_or_create(
        user=request.user, conversation=conversation
    )
    status.is_archived = False
    status.save()
    messages.success(request, 'Conversation unarchived.')
    return redirect('inbox')