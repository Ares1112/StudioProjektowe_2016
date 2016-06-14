# coding=utf-8
from __future__ import unicode_literals

from django.db import models


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
    grupa = models.ForeignKey(Grupa)

    def __unicode__(self):
        return self.numer_telefonu

    class Meta:
        verbose_name_plural = u"Turyści"
