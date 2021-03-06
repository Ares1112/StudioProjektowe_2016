# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-24 11:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourist_app', '0005_auto_20160624_1217'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grupa',
            options={'verbose_name': 'Grupa', 'verbose_name_plural': 'Grupy'},
        ),
        migrations.AlterModelOptions(
            name='niedzwiedz',
            options={'verbose_name': 'Nied\u017awied\u017a', 'verbose_name_plural': 'Nied\u017awiedzie'},
        ),
        migrations.AlterModelOptions(
            name='turysta',
            options={'verbose_name': 'Turysta', 'verbose_name_plural': 'Tury\u015bci'},
        ),
        migrations.AlterModelOptions(
            name='zagrozenieturysty',
            options={'verbose_name': 'Zagrozenie turysty', 'verbose_name_plural': 'Zagrozenia turystow'},
        ),
        migrations.AlterField(
            model_name='grupa',
            name='lider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='tourist_app.Turysta', verbose_name='Lider'),
        ),
        migrations.AlterField(
            model_name='grupa',
            name='nazwa',
            field=models.TextField(verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='niedzwiedz',
            name='identyfikator',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Identyfikator'),
        ),
        migrations.AlterField(
            model_name='niedzwiedz',
            name='pozycja_E',
            field=models.FloatField(verbose_name='Pozycja E'),
        ),
        migrations.AlterField(
            model_name='niedzwiedz',
            name='pozycja_N',
            field=models.FloatField(verbose_name='Pozycja N'),
        ),
        migrations.AlterField(
            model_name='turysta',
            name='grupa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tourist_app.Grupa', verbose_name='Grupa'),
        ),
        migrations.AlterField(
            model_name='turysta',
            name='numer_telefonu',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Numer telefonu'),
        ),
        migrations.AlterField(
            model_name='turysta',
            name='ostatni_ruch',
            field=models.DateTimeField(verbose_name='Ostatni ruch'),
        ),
        migrations.AlterField(
            model_name='turysta',
            name='pozycja_E',
            field=models.FloatField(verbose_name='Pozycja E'),
        ),
        migrations.AlterField(
            model_name='turysta',
            name='pozycja_N',
            field=models.FloatField(verbose_name='Pozycja N'),
        ),
        migrations.AlterField(
            model_name='zagrozenieturysty',
            name='turysta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourist_app.Turysta', verbose_name='Turysta'),
        ),
        migrations.AlterField(
            model_name='zagrozenieturysty',
            name='zagrozenie',
            field=models.CharField(choices=[('np', 'Mo\u017cliwe zas\u0142abniecie, wy\u015blij drona'), ('sz', 'Turysta w strefie zagro\u017cenia'), ('oog', 'Turysta oddali\u0142 si\u0119 od lidera grupy'), ('n', 'Nied\u017awied\u017a blisko turysty')], max_length=255, verbose_name='Zagro\u017cenie'),
        ),
    ]
