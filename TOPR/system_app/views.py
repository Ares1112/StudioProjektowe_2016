from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import StrefaZagrozenia, Szlak, Pogoda
from satispy import Variable, Cnf 
from satispy.solver import Minisat
from sattable import tableLevel2

@login_required
def home_view(request):
    return render(request, 'dashboard.html', {'danger_zones': StrefaZagrozenia.objects.all()})

@login_required
def weather_view(request):
    return render(request, 'weather.html')

@login_required
def sat_view(request):
    routes = Szlak.objects.all()
    return_routes = []

    t1 = Variable('temp1') 
    t2 = Variable('temp2') 
    t3 = Variable('temp3')
    
    d1 = Variable('trudnosc1') 
    d2 = Variable('trudnosc2') 
    d3 = Variable('trudnosc3')
    d4 = Variable('trudnosc4')
    
    w1 = Variable('wiatr1') 
    w2 = Variable('wiatr2') 
    w3 = Variable('wiatr3')

    m1 = Variable('mgla1')
    m2 = Variable('mgla2')
    m3 = Variable('mgla3')
    
    r1 = Variable('deszcz1')
    r2 = Variable('deszcz2')
    r3 = Variable('deszcz3')
    
    l1 = Variable('lawina1')
    l2 = Variable('lawina2')
    l3 = Variable('lawina3')
    l4 = Variable('lawina4')
    l5 = Variable('lawina5')
    
    solver = Minisat()
    
    
    RightP = r1
    Right = r1
    fst = True
    for val in tableLevel2:
        if val[0] == 1:
            RightP = d1 & -d2 & -d3 & -d4
        elif val[0] == 2:
            RightP = -d1 & d2 & -d3 & -d4
        elif val[0] == 3:
            RightP = -d1 & -d2 & d3 & -d4
        elif val[0] == 4:
            RightP = -d1 & -d2 & -d3 & d4
            
        if val[1] in (0, 1):
            RightP &= w1 & w2 & w3
        elif val[1] == 2:
            RightP &= -w1 & w2 & w3
        elif val[1] == 3:
            RightP &= -w1 & -w2 & w3
            
        if val[2] in (0, 1):
            RightP &= m1 & m2 & m3
        elif val[2] == 2:
            RightP &= -m1 & m2 & m3
        elif val[2] == 3:
            RightP &= -m1 & -m2 & m3
            
        if val[3] in (0, 1):
            RightP &= t1 & t2 & t3
        elif val[3] == 2:
            RightP &= -t1 & t2 & t3
        elif val[3] == 3:
            RightP &= -t1 & -t2 & t3

        if val[4] in (0, 1):
            RightP &= r1 & r2 & r3
        elif val[4] == 2:
            RightP &= -r1 & r2 & r3
        elif val[4] == 3:
            RightP &= -r1 & -r2 & r3
            
        if val[5] in (0, 1):
            RightP &= l1 & l2 & l3 & l4 & l5
        elif val[5] == 2:
            RightP &= -l1 & l2 & l3 & l4 & l5
        elif val[5] == 3:
            RightP &= -l1 & -l2 & l3 & l4 & l5
        elif val[5] == 4:
            RightP &= -l1 & -l2 & -l3 & l4 & l5
        elif val[5] == 5:
            RightP &= -l1 & -l2 & -l3 & -l4 & l5
            
        if fst:
            Right = RightP
            fst = False
        if not fst:
            Right |= (RightP)
    for szlak in routes:
        pogoda = Pogoda.objects.filter(szlak__id=szlak.id).order_by('-czas')[0]
        Actual = d1
        if szlak.trudnosc == 1:
            Actual = d1 & -d2 & -d3 & -d4
        elif szlak.trudnosc == 2:
            Actual = -d1 & d2 & -d3 & -d4
        elif szlak.trudnosc == 3:
            Actual = -d1 & -d2 & d3 & -d4
        elif szlak.trudnosc == 4:
            Actual = -d1 & -d2 & -d3 & d4
        
        if pogoda.deszcz.wiatr.stopien in (0, 1):
            Actual &= w1 & -w2 & -w3
        elif pogoda.deszcz.wiatr.stopien == 2:
            Actual &= w1 & w2 & -w3
        elif pogoda.deszcz.wiatr.stopien == 3:
            Actual &= w1 & w2 & w3
            
        if pogoda.mgla.stopien in (0, 1):
            Actual &= m1 & -m2 & -m3
        elif pogoda.mgla.stopien == 2:
            Actual &= m1 & m2 & -m3
        elif pogoda.mgla.stopien == 3:
            Actual &= m1 & m2 & m3
            
        if pogoda.temperatura.stopien in (0, 1):
            Actual &= t1 & -t2 & -t3
        elif pogoda.temperatura.stopien == 2:
            Actual &= t1 & t2 & -t3
        elif pogoda.temperatura.stopien == 3:
            Actual &= t1 & t2 & t3

        if pogoda.deszcz.stopien in (0, 1):
            Actual &= r1 & -r2 & -r3
        elif pogoda.deszcz.stopien == 2:
            Actual &= r1 & r2 & -r3
        elif pogoda.deszcz.stopien == 3:
            Actual &= r1 & r2 & r3
            
        if pogoda.lawina.stopien in (0, 1):
            Actual &= l1 & -l2 & -l3 & -l4 & -l5
        elif pogoda.lawina.stopien == 2:
            Actual &= l1 & l2 & -l3 & -l4 & -l5
        elif pogoda.lawina.stopien == 3:
            Actual &= l1 & l2 & l3 & -l4 & -l5
        elif pogoda.lawina.stopien == 4:
            Actual &= l1 & l2 & l3 & l4 & -l5
        elif pogoda.lawina.stopien == 5:
            Actual &= l1 & l2 & l3 & l4 & l5
        Actual = d1 & -d2 & -d3 & -d4 & w1 & -w2 & -w3 & m1 & m2 & -m3
        Right = d1 & -d2 & -d3 & -d4 & -w1 & w2 & w3 & -m1 & -m2 & m3
        Alarm = ((Actual) >> (Right)) ^ Actual
        solution = solver.solve(Alarm)
        print szlak, solution.success, solution[d1], solution[d2], solution[d3], solution[d4], solution[w1], solution[w2], solution[w3], solution[m1], solution[m2], solution[m3]

            
    return render(request, 'sat.html', {'routes': return_routes})