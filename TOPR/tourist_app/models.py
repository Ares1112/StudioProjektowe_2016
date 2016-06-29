# coding=utf-8
from __future__ import unicode_literals

from django.utils import timezone
import datetime
from django.utils.translation import ugettext_lazy as _

from django.db import models
from .tools import haversine
from system_app.models import StrefaZagrozenia


class Grupa(models.Model):
    lider = models.ForeignKey('Turysta', related_name='+', verbose_name=_('Lider'))
    nazwa = models.TextField(verbose_name=_('Nazwa'))

    def __unicode__(self):
        return self.nazwa

    class Meta:
        verbose_name = _('Grupa')
        verbose_name_plural = _('Grupy')


class Turysta(models.Model):
    numer_telefonu = models.CharField(max_length=20, primary_key=True ,verbose_name=_('Numer telefonu'))
    pozycja_N = models.FloatField(verbose_name=_('Pozycja N'))
    pozycja_E = models.FloatField(verbose_name=_('Pozycja E'))
    ostatni_ruch = models.DateTimeField(verbose_name=_('Ostatni ruch'))
    grupa = models.ForeignKey(Grupa, blank=True, null=True, verbose_name=_('Grupa'))
    
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
        if self.grupa and not self.grupa.lider == self:
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
        # niedzwiedz
        niedzwiedzie = Niedzwiedz.objects.all()
        anystrefa = False
        for niedzwiedz in niedzwiedzie:
            if float(haversine(self.pozycja_N, self.pozycja_E, niedzwiedz.pozycja_N, niedzwiedz.pozycja_E)) <= 0.5:
                anystrefa = True
                zagrozenie = ZagrozenieTurysty.objects.filter(turysta__numer_telefonu=self.numer_telefonu, zagrozenie='n').first()
                if not zagrozenie:
                    obj = ZagrozenieTurysty()
                    obj.turysta = self
                    obj.zagrozenie = 'n'
                    obj.save()
                break
        if not anystrefa:
            zagrozenie = ZagrozenieTurysty.objects.filter(turysta__numer_telefonu=self.numer_telefonu, zagrozenie='n').first()
            if zagrozenie:
                zagrozenie.delete()
        super(Turysta, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.numer_telefonu

    class Meta:
        verbose_name = _('Turysta')
        verbose_name_plural = _(u'Turyści')


ZAGROZENIA = (
    ('np', _(u'Możliwe zasłabniecie, wyślij drona')), 
    ('sz', _(u'Turysta w strefie zagrożenia')), 
    ('oog', _(u'Turysta oddalił się od lidera grupy')),
    ('n', _(u'Niedźwiedź blisko turysty')),
    )
 
class ZagrozenieTurysty(models.Model):
    turysta = models.ForeignKey(Turysta, verbose_name=_('Turysta'))
    zagrozenie = models.CharField(max_length=255, choices=ZAGROZENIA, verbose_name=_(u'Zagrożenie'))
    
    def __unicode__(self):
        return self.turysta.numer_telefonu

    class Meta:
        verbose_name = _('Zagrozenie turysty')
        verbose_name_plural = _('Zagrozenia turystow')
        
class Niedzwiedz(models.Model):
    pozycja_N = models.FloatField(verbose_name=_('Pozycja N'))
    pozycja_E = models.FloatField(verbose_name=_('Pozycja E'))
    identyfikator = models.CharField(max_length=100, primary_key=True, verbose_name=_('Identyfikator'))
    
    def __unicode__(self):
        return self.identyfikator
    
    class Meta:
        verbose_name = _(u'Niedźwiedź')
        verbose_name_plural = _(u'Niedźwiedzie')