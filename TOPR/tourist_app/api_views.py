from django.http import HttpResponse, JsonResponse
from .tools import generate_KML_for_tourists
from .models import Turysta, ZagrozenieTurysty


def api_get_tourists(request):
    kml = generate_KML_for_tourists(Turysta.objects.all())
    return HttpResponse(kml)
	

def api_get_tourist_danger_info(request):
    all_dangers = ZagrozenieTurysty.objects.all()
    info = [{'key': danger.id, 'telefon': danger.turysta.numer_telefonu, 'zagrozenie': danger.get_zagrozenie_display()} for danger in all_dangers]
    return JsonResponse(info, safe=False)