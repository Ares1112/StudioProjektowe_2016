from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import StrefaZagrozenia

@login_required
def home_view(request):
    return render(request, 'dashboard.html', {'danger_zones': StrefaZagrozenia.objects.all()})

@login_required
def weather_view(request):
    return render(request, 'weather.html')

@login_required
def sat_view(request):
    return render(request, 'sat.html', {'results': 'TEST'})