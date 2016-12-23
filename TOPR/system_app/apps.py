# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import StrefaZagrozenia, Szlak, Pogoda
from sattable import tableLevel2, tableLevel3, tableLevel4, tableLevel5

class SystemAppConfig(AppConfig):
    name = 'system_app'

@login_required
def sat_viev(request):
    routes = Szlak.objects.all()
    return_routes = []
    for route in routes:
        isFound = False
        pogoda = Pogoda.objects.filter(szlak__id=route.id).order_by('-czas')[0]
        print pogoda.wiatr.stopien, pogoda.mgla.stopien, pogoda.temperatura.stopien, pogoda.lawina.stopien
        for elem in tableLevel5:
            if elem[0] == route.trudnosc and elem[1] <= pogoda.wiatr.stopien and elem[2] <= pogoda.mgla.stopien \
            and elem[3] <= pogoda.temperatura.stopien and elem[4] <= pogoda.deszcz.stopien and elem[5] <= pogoda.lawina.stopien:
                return_routes.append([route, u"Przechwycenie turystów"])
                isFound = True
                break
        if not isFound:
            for elem in tableLevel4:
                if elem[0] == route.trudnosc and elem[1] <= pogoda.wiatr.stopien and elem[2] <= pogoda.mgla.stopien \
                and elem[3] <= pogoda.temperatura.stopien and elem[4] <= pogoda.deszcz.stopien and elem[5] <= pogoda.lawina.stopien:
                    return_routes.append([route, u"Wysłanie drona do zbadania sytuacji i podjęcia decyzji o wysłaniu ekipy ratowniczej"])
                    isFound = True
                    break
        if not isFound:
            for elem in tableLevel3:
                if elem[0] == route.trudnosc and elem[1] <= pogoda.wiatr.stopien and elem[2] <= pogoda.mgla.stopien \
                and elem[3] <= pogoda.temperatura.stopien and elem[4] <= pogoda.deszcz.stopien and elem[5] <= pogoda.lawina.stopien:
                    return_routes.append([route, u"Wysłanie drona w celu lepszego monitorowania szlaku"])
                    isFound = True
                    break
        if not isFound:
            for elem in tableLevel2:
                if elem[0] == route.trudnosc and elem[1] <= pogoda.wiatr.stopien and elem[2] <= pogoda.mgla.stopien \
                and elem[3] <= pogoda.temperatura.stopien and elem[4] <= pogoda.deszcz.stopien and elem[5] <= pogoda.lawina.stopien:
                    return_routes.append([route, u"Monitorowanie turystów na zagrożonych obszarach"])
                    isFound = True
                    break
        if not isFound:
            return_routes.append([route, "System monitoruje"])
            
            
    return render(request, 'sat.html', {'routes': return_routes})