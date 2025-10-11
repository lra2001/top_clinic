from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm
from django.http import JsonResponse
from datetime import datetime, time, timedelta


# Create your views here.

def home(request):
    return render(request, 'home.html')

def specialties(request):
    return render(request, 'specialties.html')

def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='login')
def appointments(request):
    if hasattr(request.user, 'profile'):
        role = request.user.profile.role
    else:
        role = None

    if role == 'doctor':
        messages.info(request, "Doctors cannot book appointments.")
        return redirect('home')
    elif role == 'patient':
        # Patient booking logic
        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                specialty = form.cleaned_data['specialty']
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']
                if Appointment.objects.filter(date=date, time=time, specialty=specialty).exists():
                    messages.error(request, "This slot is already booked.")
                else:
                    appointment = form.save(commit=False)
                    appointment.user = request.user
                    appointment.save()
                    messages.success(request, "Appointment booked successfully!")
                    return redirect('appointments')
        else:
            form = AppointmentForm()
        return render(request, 'appointments.html', {'form': form})
    else:
        messages.info(request, "Only patients can book appointments.")
        return redirect('home')

def get_available_slots(request):
    date_str = request.GET.get('date')
    specialty = request.GET.get('specialty')

    if not date_str or not specialty:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    start_time = time(9, 0)
    end_time = time(17, 0)
    interval = timedelta(minutes=30)

    slots = []
    current = datetime.combine(date, start_time)
    end = datetime.combine(date, end_time)

    # Get already booked times
    booked = set(
        Appointment.objects.filter(date=date, specialty=specialty).values_list('time', flat=True)
    )

    while current < end:
        slot_time = current.time()
        slots.append({
            'time': slot_time.strftime('%H:%M'),
            'available': slot_time not in booked
        })
        current += interval

    return JsonResponse({'slots': slots})