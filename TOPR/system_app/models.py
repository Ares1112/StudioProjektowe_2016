# coding=utf-8    
    
from __future__ import unicode_literals    
    
import datetime    
    
from django.core.validators import MinValueValidator    
from django.db import models    
from django.utils import timezone    
    
from django.utils.translation import ugettext_lazy as _    
    
KOLORY_SZLAKOW = (('zo', _(u'żółty')), ('n', _('niebieski')), ('z', _('zielony')), ('cza', _('czarny')), ('cze', _('czerwony')))    
    
    
class Wiatr(models.Model):    
    stopien = models.IntegerField(validators=[MinValueValidator(0)], blank=False, verbose_name=_(u'Stopień'))    
    predkosc_minimalna = models.IntegerField(validators=[MinValueValidator(0)], blank=False, verbose_name=_(u'Prędkość minimalna'))    
    predkosc_maksymalna = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_(u'Prędkość maksymalna'))    
    
    def __unicode__(self):    
        return str(self.stopien)    
    
    class Meta:    
        verbose_name=_(u'Stopień wiatru')    
        verbose_name_plural=_(u'Stopnie wiatru')    
    
    
class Mgla(models.Model):    
    stopien = models.IntegerField(validators=[MinValueValidator(0)], blank=False, verbose_name=_(u'Stopień'))    
    opis = models.TextField(verbose_name=_(u'Opis'))    
    
    def __unicode__(self):    
        return str(self.stopien)    
    
    class Meta:    
        verbose_name=_(u'Stopień mgły')    
        verbose_name_plural = _(u'Stopnie mgły')    
    
    
class Temperatura(models.Model):    
    stopien = models.IntegerField(validators=[MinValueValidator(0)], blank=False, verbose_name=_(u'Stopień'))    
    powyzej = models.IntegerField(verbose_name=_(u'Powyżej'))    
    ponizej = models.IntegerField(verbose_name=_(u'Poniżej'))    
    
    def __unicode__(self):    
        return str(self.stopien)    
    
    class Meta:    
        verbose_name=_(u'Stopień temperatury')    
        verbose_name_plural = _(u'Stopnie temperatury')    
    
    
class Deszcz(models.Model):    
    stopien = models.IntegerField(validators=[MinValueValidator(0)], blank=False, verbose_name=_(u'Stopień'))    
    deszcz_minimalny = models.IntegerField(validators=[MinValueValidator(0)], blank=False, verbose_name=_(u'Deszcz minimanly'))    
    deszcz_maksymalny = models.IntegerField(validators=[MinValueValidator(0)], verbose_name=_(u'Deszcz maksymalny'))    
    wiatr = models.ForeignKey(Wiatr, verbose_name=_(u'Wiatr'))    
    
    def __unicode__(self):    
        return str(self.stopien)    
    
    class Meta:    
        verbose_name=_(u'Stopień deszczu')    
        verbose_name_plural =_(u'Stopnie deszczu')    
    
    
class Lawina(models.Model):    
    stopien = models.IntegerField(validators=[MinValueValidator(0)], blank=False, verbose_name=_(u'Stopień'))    
    opis = models.TextField(verbose_name=_(u'Opis'))    
    
    def __unicode__(self):    
        return str(self.stopien)    
    
    class Meta:    
        verbose_name=_(u'Stopień lawiny')    
        verbose_name_plural = _(u'Stopnie lawiny')    
    
    
DZIALANIA = (    
    ('sm', _('System monitoruje')),    
    ('mt', _(u'Monitorowanie turystów na zagrożonych obszarach')),     
    ('wd', _(u'Wysłanie drona w celu lepszego monitorowania szlaku')),    
    ('wder', _(u'Wysłanie drona do zbadania sytuacji i podjęcia decyzji o wysłaniu ekipy ratowniczej')),
    ('pt', _(u'Przechwycenie turystów'))    
    )    
            
class StanAlarmowy(models.Model):    
    poziom = models.IntegerField(validators=[MinValueValidator(0)], blank=False, verbose_name=_(u'Poziom'))    
    dzialanie = models.CharField(max_length=255, blank=False, choices=DZIALANIA, default='sm', verbose_name=_(u'Działanie'))    
    
    def __unicode__(self):    
        return str(self.poziom)    
    
    class Meta:    
        verbose_name=_(u'Stan alarmowy')    
        verbose_name_plural = _(u'Stany alarmowe')    
    
    
class Szlak(models.Model):    
    stan_alarmowy = models.ForeignKey(StanAlarmowy, verbose_name=_(u'Stan alarmowy'))    
    KML = models.TextField(blank=False)    
    trudnosc = models.IntegerField(validators=[MinValueValidator(1)], verbose_name=_(u'Trudność'))    
    kolor = models.CharField(max_length=255, choices=KOLORY_SZLAKOW, verbose_name=_(u'Kolor'))    
    nazwa = models.CharField(max_length=255, verbose_name=_(u'Nazwa'))    
    
    def __unicode__(self):    
        return self.nazwa    
    
    class Meta:    
        verbose_name=_(u'Szlak')    
        verbose_name_plural = _(u'Szlaki')    
    
    
class Pogoda(models.Model):    
    wiatr = models.ForeignKey(Wiatr, verbose_name=_(u'Stopień wiatru'))    
    mgla = models.ForeignKey(Mgla, verbose_name=_(u'Stopień mgły'))    
    temperatura = models.ForeignKey(Temperatura, verbose_name=_(u'Stopień temperatury'))    
    deszcz = models.ForeignKey(Deszcz, verbose_name=_(u'Stopień deszczu'))    
    lawina = models.ForeignKey(Lawina, verbose_name=_(u'Stopień lawiny'))    
    czas = models.DateTimeField(blank=False, verbose_name=_(u'Czas'))    
    szlak = models.ForeignKey(Szlak, null=True, verbose_name=_(u'Szlak'))    
    
    def __unicode__(self):    
        return str(self.czas)    
    
    def zwroc_stan_alarmowy(self):    
        stopnie_pogoda = self.wiatr.stopien + self.mgla.stopien + self.temperatura.stopien + self.deszcz.stopien + self.lawina.stopien    
        skala = round((stopnie_pogoda + self.szlak.trudnosc) / 4.0)    
        return StanAlarmowy.objects.order_by('poziom').filter(poziom__gte=skala).first()    
    
    def save(self, *args, **kwargs):    
        if self.czas > timezone.now() - datetime.timedelta(minutes=5):    
            self.szlak.stan_alarmowy = self.zwroc_stan_alarmowy()    
            self.szlak.save()    
        super(Pogoda, self).save(*args, **kwargs)    
    
    class Meta:    
        verbose_name=_(u'Pogoda')    
        verbose_name_plural = _(u'Pogody')    
          
            
class StrefaZagrozenia(models.Model):    
    pozycja_N = models.FloatField(verbose_name=_(u'Pozycja N'))    
    pozycja_E = models.FloatField(verbose_name=_(u'Pozycja E'))    
    promien = models.IntegerField(help_text = 'jednostka [m]', verbose_name=_(u'Promień'))    
    nazwa = models.CharField(max_length=255, verbose_name=_(u'Nazwa'))    
	    
    def __unicode__(self):
        return self.nazwa
    
    class Meta:
        verbose_name=_(u'Strefa zagrożenia')
        verbose_name_plural=_(u'Strefy zagrożenia')