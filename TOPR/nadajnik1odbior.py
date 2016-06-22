import os
import sys
import django
sys.path.append(os.path.join(os.path.dirname(__file__), "TOPR"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TOPR.settings")
django.setup()

from tourist_app.models import Turysta

from kafka import KafkaConsumer
from django.utils import timezone

consumer = KafkaConsumer('nadajnik1', auto_offset_reset='earliest',
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'])
for message in consumer:
    if message.value=="outofrange":
        try:
            tourist = Turysta.objects.get(numer_telefonu=message.key)
            tourist.delete()
        except Turysta.DoesNotExist:
            pass
        continue
    position = message.value.split(',')
    try:
        tourist = Turysta.objects.get(numer_telefonu=message.key)
        print tourist.numer_telefonu, tourist.pozycja_N, tourist.pozycja_E, position[0], position[1]
        if tourist.pozycja_N != float(position[0]) or tourist.pozycja_E != float(position[1]):
            tourist.pozycja_N = position[0]
            tourist.pozycja_E = position[1]
            tourist.ostatni_ruch = timezone.now()
    except Turysta.DoesNotExist:
        tourist = Turysta(numer_telefonu=message.key, pozycja_N=position[0], pozycja_E=position[1], ostatni_ruch=timezone.now())
    tourist.save()
