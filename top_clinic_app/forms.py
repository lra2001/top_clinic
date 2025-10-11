from django import forms
from .models import Appointment, SPECIALTY_CHOICES
import datetime

class AppointmentForm(forms.ModelForm):
    specialty = forms.ChoiceField(choices=SPECIALTY_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'form-control',
        'min': '',
    }))
    time = forms.ChoiceField(choices=[], widget=forms.Select(attrs={
        'class': 'form-select'
    }))

    class Meta:
        model = Appointment
        fields = ['specialty', 'date', 'time']