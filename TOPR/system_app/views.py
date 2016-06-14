from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Szlak, Pogoda

@login_required
def home_view(request):
    return render(request, 'dashboard.html', {'szlaki': Szlak.objects.all()})

@login_required
def weather_view(request):
    return render(request, 'weather.html')
