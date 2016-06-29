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

from tourist_app.models import Turysta, Niedzwiedz

uczestnik = Turysta(numer_telefonu='323456789', pozycja_N=19.5, pozycja_E=49.58, ostatni_ruch=timezone.now())
uczestnik.save()

y = 49.58
y2 = 49.565
while True:
    producer.send(topic='nadajnik1', key='323456789', value=b'19.5,'+str(y))
    producer.send(topic='nadajnik1', key='niedzwiedz1', value=b'19.5,'+str(y2))
    producer.flush()
    y -= 0.0002
    y2 += 0.0002
    time.sleep(3)

