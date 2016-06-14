from django.http import HttpResponse, JsonResponse
from .tools import generate_KML
from .models import Szlak, Pogoda

def api_get_routes(request):
    selected_colors = request.GET.get('colors', 'zo,n,z,cza,cze').split(',')
    selected_colors = [color.strip() for color in selected_colors]
    kml = generate_KML(Szlak.objects.filter(kolor__in=selected_colors))
    return HttpResponse(kml)

def api_get_routes_info(request):
    all_routes = Szlak.objects.all()
    info = [{'key': szlak.id, 'nazwa': szlak.nazwa, 'poziom': szlak.stan_alarmowy.poziom,
             'kolor': szlak.get_kolor_display(), 'dzialanie': szlak.stan_alarmowy.dzialanie} for szlak in all_routes]
    return JsonResponse(info, safe=False)

def api_get_weather_info(request):
    all_weathers = Pogoda.objects.all().order_by('-czas')
    tmp = []
    all_w = []
    for w in all_weathers:
        if w.szlak.nazwa not in tmp:
            tmp.append(w.szlak.nazwa)
            all_w.append(w)
    info = [{'key': pogoda.id, 'wiatr': pogoda.wiatr.stopien, 'mgla': pogoda.mgla.stopien, 'temperatura': pogoda.temperatura.stopien,
             'deszcz': pogoda.deszcz.stopien, 'lawina': pogoda.lawina.stopien, 'czas': pogoda.czas, 'szlak': pogoda.szlak.nazwa} for pogoda in all_w]
    return JsonResponse(info, safe=False)