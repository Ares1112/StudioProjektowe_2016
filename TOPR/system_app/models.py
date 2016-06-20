# coding=utf-8

from __future__ import unicode_literals

import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

KOLORY_SZLAKOW = (('zo', u'żółty'), ('n', 'niebieski'), ('z', 'zielony'), ('cza', 'czarny'), ('cze', 'czerwony'))


class Wiatr(models.Model):
    stopien = models.IntegerField(validators=[MinValueValidator(0)], blank=False)
    predkosc_minimalna = models.IntegerField(validators=[MinValueValidator(0)], blank=False)
    predkosc_maksymalna = models.IntegerField(validators=[MinValueValidator(0)])

    def __unicode__(self):
        return str(self.stopien)

    class Meta:
        verbose_name_plural = 'Stopnie wiatru'


class Mgla(models.Model):
    stopien = models.IntegerField(validators=[MinValueValidator(0)], blank=False)
    opis = models.TextField()

    def __unicode__(self):
        return str(self.stopien)

    class Meta:
        verbose_name_plural = u'Stopnie mgły'


class Temperatura(models.Model):
    stopien = models.IntegerField(validators=[MinValueValidator(0)], blank=False)
    powyzej = models.IntegerField()
    ponizej = models.IntegerField()

    def __unicode__(self):
        return str(self.stopien)

    class Meta:
        verbose_name_plural = 'Stopnie temperatury'


class Deszcz(models.Model):
    stopien = models.IntegerField(validators=[MinValueValidator(0)], blank=False)
    deszcz_minimalny = models.IntegerField(validators=[MinValueValidator(0)], blank=False)
    deszcz_maksymalny = models.IntegerField(validators=[MinValueValidator(0)])
    wiatr = models.ForeignKey(Wiatr)

    def __unicode__(self):
        return str(self.stopien)

    class Meta:
        verbose_name_plural = 'Stopnie deszczu'


class Lawina(models.Model):
    stopien = models.IntegerField(validators=[MinValueValidator(0)], blank=False)
    opis = models.TextField()

    def __unicode__(self):
        return str(self.stopien)

    class Meta:
        verbose_name_plural = 'Stopnie lawiny'


class StanAlarmowy(models.Model):
    poziom = models.IntegerField(validators=[MinValueValidator(0)], blank=False)
    dzialanie = models.CharField(max_length=255, blank=False)

    def __unicode__(self):
        return str(self.poziom)

    class Meta:
        verbose_name_plural = 'Stany alarmowe'


class Szlak(models.Model):
    stan_alarmowy = models.ForeignKey(StanAlarmowy)
    KML = models.TextField(blank=False)
    trudnosc = models.IntegerField(validators=[MinValueValidator(1)])
    kolor = models.CharField(max_length=255, choices=KOLORY_SZLAKOW)
    nazwa = models.CharField(max_length=255)

    def __unicode__(self):
        return self.nazwa

    class Meta:
        verbose_name_plural = 'Szlaki'


class Pogoda(models.Model):
    wiatr = models.ForeignKey(Wiatr)
    mgla = models.ForeignKey(Mgla)
    temperatura = models.ForeignKey(Temperatura)
    deszcz = models.ForeignKey(Deszcz)
    lawina = models.ForeignKey(Lawina)
    czas = models.DateTimeField(blank=False)
    szlak = models.ForeignKey(Szlak, null=True)

    def __unicode__(self):
        return str(self.czas)

    def zwroc_stan_alarmowy(self):
        stopnie_pogoda = self.wiatr.stopien + self.mgla.stopien + \
                         self.temperatura.stopien + self.deszcz.stopien + self.lawina.stopien
        skala = round((stopnie_pogoda + self.szlak.trudnosc) / 4.0)
        return StanAlarmowy.objects.order_by('poziom').filter(poziom__gte=skala).first()

    def save(self, *args, **kwargs):
        if self.czas > timezone.now() - datetime.timedelta(minutes=5):
            self.szlak.stan_alarmowy = self.zwroc_stan_alarmowy()
            self.szlak.save()
        super(Pogoda, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Pogody'
      
        
class StrefaZagrozenia(models.Model):
	pozycja_N = models.FloatField()
	pozycja_E = models.FloatField()
	promien = models.IntegerField(help_text = 'jednostka [m]')
	nazwa = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.nazwa
		
	class Meta:
		verbose_name_plural = 'Strefy zagrozenia'
