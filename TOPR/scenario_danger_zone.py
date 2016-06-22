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

from tourist_app.models import Turysta
from system_app.models import StrefaZagrozenia

zagr = StrefaZagrozenia.objects.filter(nazwa='testowa').first()
if zagr:
    zagr.pozycja_N=19.5343
    zagr.pozycja_E=49.575
    zagr.promien=100
else: 
    zagr = StrefaZagrozenia(pozycja_N=19.5343, pozycja_E=49.575, promien=100, nazwa='testowa')
zagr.save()

srodek = Turysta(numer_telefonu='223456789', pozycja_N=19.5343, pozycja_E=49.575, ostatni_ruch=timezone.now())
srodek.save()

uczestnik = Turysta(numer_telefonu='2234567891', pozycja_N=19.5343, pozycja_E=49.573, ostatni_ruch=timezone.now())
uczestnik.save()

y = 49.574
while True:
    producer.send(topic='nadajnik1', key='2234567891', value=b'19.5343,'+str(y))
    producer.flush()
    y += 0.0001
    time.sleep(6)

