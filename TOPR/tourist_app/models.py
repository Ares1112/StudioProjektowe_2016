# coding=utf-8
from __future__ import unicode_literals

from django.utils import timezone
import datetime

from django.db import models
from .tools import haversine
from system_app.models import StrefaZagrozenia


class Grupa(models.Model):
    lider = models.ForeignKey('Turysta', related_name='+')
    nazwa = models.TextField()

    def __unicode__(self):
        return self.nazwa

    class Meta:
        verbose_name_plural = u"Grupy"


class Turysta(models.Model):
    numer_telefonu = models.CharField(max_length=20, primary_key=True)
    pozycja_N = models.FloatField()
    pozycja_E = models.FloatField()
    ostatni_ruch = models.DateTimeField()
    grupa = models.ForeignKey(Grupa, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # nieprzytomnosc
        if self.ostatni_ruch < timezone.now() - datetime.timedelta(minutes=15):
            zagrozenie = ZagrozenieTurysty.objects.filter(turysta=self, zagrozenie='np').first()
            if not zagrozenie:
                obj = ZagrozenieTurysty()
                obj.turysta = self
                obj.zagrozenie = 'np'
                obj.save()
        else:
            zagrozenie = ZagrozenieTurysty.objects.filter(turysta=self, zagrozenie='np').first()
            if zagrozenie:
                zagrozenie.delete()
        # strefy zagrozenia
        strefy = StrefaZagrozenia.objects.all()
        anystrefa = False
        for strefa in strefy:
            if float(haversine(self.pozycja_N, self.pozycja_E, strefa.pozycja_N, strefa.pozycja_E)) <= float(strefa.promien)/1000.0:
                anystrefa = True
                zagrozenie = ZagrozenieTurysty.objects.filter(turysta__numer_telefonu=self.numer_telefonu, zagrozenie='sz').first()
                if not zagrozenie:
                    obj = ZagrozenieTurysty()
                    obj.turysta = self
                    obj.zagrozenie = 'sz'
                    obj.save()
                break
        if not anystrefa:
            zagrozenie = ZagrozenieTurysty.objects.filter(turysta__numer_telefonu=self.numer_telefonu, zagrozenie='sz').first()
            if zagrozenie:
                zagrozenie.delete()
        # odlaczenie od grupy
        if self.grupa or not self.grupa.lider == self:
            if haversine(self.pozycja_N, self.pozycja_E, self.grupa.lider.pozycja_N, self.grupa.lider.pozycja_E) >= 0.2:
                zagrozenie = ZagrozenieTurysty.objects.filter(turysta=self, zagrozenie='oog').first()
                if not zagrozenie:
                    obj = ZagrozenieTurysty()
                    obj.turysta = self
                    obj.zagrozenie = 'oog'
                    obj.save()
            else:
                zagrozenie = ZagrozenieTurysty.objects.filter(turysta=self, zagrozenie='oog').first()
                if zagrozenie:
                    zagrozenie.delete()
        else:
            zagrozenie = ZagrozenieTurysty.objects.filter(turysta=self, zagrozenie='oog').first()
            if zagrozenie:
                zagrozenie.delete()
                
        super(Turysta, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.numer_telefonu

    class Meta:
        verbose_name_plural = u"Turyści"


ZAGROZENIA = (
    ('np', u'Mozliwe zaslabniecie, wyslij drona'), 
    ('sz', u'Turysta w strefie zagrozenia'), 
    ('oog', u'Turysta oddalil sie od lidera grupy')
    )
 
class ZagrozenieTurysty(models.Model):
    turysta = models.ForeignKey(Turysta)
    zagrozenie = models.CharField(max_length=255, choices=ZAGROZENIA)
    
    def __unicode__(self):
            return self.turysta.numer_telefonu

    class Meta:
        verbose_name_plural = u"Zagrozenia turystow"