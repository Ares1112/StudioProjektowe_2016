from django.http import HttpResponse
from .tools import generate_KML_for_tourists
from .models import Turysta


def api_get_tourists(request):
    kml = generate_KML_for_tourists(Turysta.objects.all())
    return HttpResponse(kml)