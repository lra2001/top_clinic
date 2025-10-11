from django import forms
from .models import Appointment
import datetime

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['specialty', 'date', 'time']

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.date.today().isoformat()})
    )