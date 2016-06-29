from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from system_app.models import StrefaZagrozenia

@login_required
def tourists_view(request):
    return render(request, 'tourists.html', {'danger_zones': StrefaZagrozenia.objects.all()})

