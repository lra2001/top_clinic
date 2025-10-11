from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def specialties(request):
    return render(request, 'specialties.html')

def contact(request):
    return render(request, 'contact.html')