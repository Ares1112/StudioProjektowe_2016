from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import StrefaZagrozenia, Szlak
from satispy import Variable, Cnf
from satispy.solver import Minisat

@login_required
def home_view(request):
    return render(request, 'dashboard.html', {'danger_zones': StrefaZagrozenia.objects.all()})

@login_required
def weather_view(request):
    return render(request, 'weather.html')

@login_required
def sat_view(request):
    v1 = Variable('v1')
    v2 = Variable('v2')
    v3 = Variable('v3')
    exp = v1 & v2 | v3
    solver = Minisat()
    solution = solver.solve(exp)
    routes = Szlak.objects.all()
    return_routes = []
    for route in routes:
        return_routes.append([route, solution]);
    return render(request, 'sat.html', {'routes': return_routes})