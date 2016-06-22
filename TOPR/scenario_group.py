from kafka import KafkaProducer
from kafka.errors import KafkaError
import os
import sys
import django
import random
import time
from django.utils import timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "TOPR")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TOPR.settings")
django.setup()
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

from tourist_app.models import Turysta, Grupa

lider = Turysta(numer_telefonu='123456789', pozycja_N=19.53410, pozycja_E=49.573, ostatni_ruch=timezone.now())
lider.save()

Grupa.objects.filter(lider=lider).delete()
grupa = Grupa(lider=lider, nazwa='Grupa testowa')
grupa.save()

uczestnik = Turysta(numer_telefonu='1234567891', pozycja_N=19.53410, pozycja_E=49.5731, ostatni_ruch=timezone.now(), grupa = grupa)
uczestnik.save()

y = 49.573
while True:
    producer.send(topic='nadajnik1', key='1234567891', value=b'19.53410,'+str(y))
    producer.flush()
    y += 0.0002
    time.sleep(6)

