from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from top_clinic_app.models import Appointment
from top_clinic_app.forms import AppointmentForm

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