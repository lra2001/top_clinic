from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, SPECIALTY_CHOICES
from .forms import AppointmentForm
from django.http import JsonResponse
from datetime import datetime, time, timedelta
from users.models import Profile
from django.views.decorators.http import require_GET


# Create your views here.

def home(request):
    return render(request, 'home.html')

def specialties(request):
    return render(request, 'specialties.html')

def contact(request):
    return render(request, 'contact.html')

@login_required(login_url='login')
def appointments(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'patient':
        messages.info(request, "Only patients can book appointments.")
        return redirect('home')

    form = AppointmentForm(request.POST or None)

    # Set today as minimum date
    today_str = datetime.today().strftime('%Y-%m-%d')
    form.fields['date'].widget.attrs['min'] = today_str

    if request.method == 'POST' and form.is_valid():
        specialty = form.cleaned_data['specialty']
        date = form.cleaned_data['date']
        time_slot = form.cleaned_data['time']

        # Choose a doctor for that specialty
        doctor_profile = Profile.objects.filter(role='doctor', specialty=specialty).first()
        if not doctor_profile:
            messages.error(request, "No doctors available for this specialty.")
            return redirect('appointments')

        if Appointment.objects.filter(date=date, time=time_slot, doctor=doctor_profile.user).exists():
            messages.error(request, "This slot is already booked.")
        else:
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor_profile.user
            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('appointments')

    return render(request, 'appointments.html', {'form': form})

@require_GET
@login_required
def get_available_slots(request):
    date_str = request.GET.get('date')
    specialty = request.GET.get('specialty')

    if not date_str or not specialty:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    start_time = time(9, 0)
    end_time = time(17, 0)
    interval = timedelta(minutes=30)

    # Get all doctors with this specialty
    doctors = Profile.objects.filter(role='doctor', specialty=specialty)
    if not doctors.exists():
        return JsonResponse({'slots': []})

    slots = []
    current = datetime.combine(date, start_time)
    end = datetime.combine(date, end_time)

    while current < end:
        slot_time = current.time()
        # Check if any doctor already has an appointment at this time
        booked = Appointment.objects.filter(date=date, specialty=specialty, time=slot_time).exists()
        slots.append({
            'time': slot_time.strftime('%H:%M'),
            'available': not booked
        })
        current += interval

    return JsonResponse({'slots': slots})

@login_required(login_url='login')
def my_appointments(request):
    if not hasattr(request.user, 'profile'):
        messages.info(request, "No profile found.")
        return redirect('home')

    if request.user.profile.role == 'patient':
        appointments = Appointment.objects.filter(patient=request.user).order_by('date', 'time')
    elif request.user.profile.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=request.user).order_by('date', 'time')
    else:
        appointments = []

    context = {
        'appointments': appointments
    }
    return render(request, 'my_appointments.html', context)

# Temp solution to run migrations from a view
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth.decorators import user_passes_test

# Only allow superusers to run this view
@user_passes_test(lambda u: u.is_superuser)
def run_migrations(request):
    try:
        call_command('migrate', interactive=False)
        return HttpResponse("✅ Migrations ran successfully!")
    except Exception as e:
        return HttpResponse(f"❌ Migration error: {str(e)}", status=500)