import os
import sys
import django
import random
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "TOPR")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TOPR.settings")
django.setup()

from django.utils import timezone

from system_app.models import Wiatr, Mgla, Temperatura, Deszcz, Lawina, Pogoda, Szlak

wiatr0 = Wiatr.objects.filter(stopien=0).first()
wiatr1 = Wiatr.objects.filter(stopien=1).first()
wiatr2 = Wiatr.objects.filter(stopien=2).first()
wiatr3 = Wiatr.objects.filter(stopien=3).first()

mgla0 = Mgla.objects.filter(stopien=0).first()
mgla1 = Mgla.objects.filter(stopien=1).first()
mgla2 = Mgla.objects.filter(stopien=2).first()
mgla3 = Mgla.objects.filter(stopien=3).first()

temperatura0 = Temperatura.objects.filter(stopien=0).first()
temperatura1 = Temperatura.objects.filter(stopien=1).first()
temperatura2 = Temperatura.objects.filter(stopien=2).first()
temperatura3 = Temperatura.objects.filter(stopien=3).first()

deszcz0 = Deszcz.objects.filter(stopien=0).first()
deszcz1 = Deszcz.objects.filter(stopien=1).first()
deszcz2 = Deszcz.objects.filter(stopien=2).first()
deszcz3 = Deszcz.objects.filter(stopien=3).first()

lawina0 = Lawina.objects.filter(stopien=0).first()
lawina1 = Lawina.objects.filter(stopien=1).first()
lawina2 = Lawina.objects.filter(stopien=2).first()
lawina3 = Lawina.objects.filter(stopien=3).first()

szlaki = Szlak.objects.all()

wiatry = (wiatr0, wiatr1, wiatr2, wiatr3)

mgly = (mgla0, mgla1, mgla2, mgla3)

temperatury = (temperatura0, temperatura1, temperatura2, temperatura3)

deszcze = (deszcz0, deszcz1, deszcz2, deszcz3)

lawiny = (lawina0, lawina1, lawina2, lawina3)

while True:
    for szlak in szlaki:
        pogoda = Pogoda(wiatr=random.choice(wiatry), mgla=random.choice(mgly), temperatura=random.choice(temperatury), deszcz=random.choice(deszcze), 
        lawina=random.choice(lawiny), czas=timezone.now(), szlak=szlak)
        pogoda.save()
        n = ('zmieniono pogode na ' + unicode(pogoda.szlak) + ' wiatr ' + unicode(pogoda.wiatr) + ' mgla ' + unicode(pogoda.mgla) + \
        ' temperatura ' + unicode(pogoda.temperatura) + ' deszcz ' + unicode(pogoda.deszcz) + ' lawina ' + unicode(pogoda.lawina)).encode('utf-8')
        print n
        time.sleep(5)