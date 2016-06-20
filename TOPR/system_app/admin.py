from django.contrib import admin
from .models import Wiatr, Mgla, Temperatura, Deszcz, Pogoda, Lawina, StanAlarmowy, Szlak, StrefaZagrozenia

@admin.register(Wiatr)
class WiatrAdmin(admin.ModelAdmin):
    list_display = ('stopien', 'predkosc_minimalna', 'predkosc_maksymalna')


@admin.register(Mgla)
class MglaAdmin(admin.ModelAdmin):
    list_display = ('stopien', 'opis')


@admin.register(Temperatura)
class TemperaturaAdmin(admin.ModelAdmin):
    list_display = ('stopien', 'powyzej', 'ponizej')

@admin.register(Deszcz)
class DeszczAdmin(admin.ModelAdmin):
    list_display = ('stopien', 'deszcz_minimalny', 'deszcz_maksymalny', 'wiatr')


@admin.register(Pogoda)
class PogodaAdmin(admin.ModelAdmin):
    list_display = ('szlak', 'wiatr', 'mgla', 'temperatura', 'deszcz', 'lawina', 'czas')


@admin.register(Lawina)
class LawinaAdmin(admin.ModelAdmin):
    list_display = ('stopien', 'opis')


@admin.register(StanAlarmowy)
class StanAlarmowyAdmin(admin.ModelAdmin):
    list_display = ('poziom', 'dzialanie')


@admin.register(Szlak)
class SzlakAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'stan_alarmowy', 'kolor', 'trudnosc')
	
@admin.register(StrefaZagrozenia)
class StrefaZagrozeniaAdmin(admin.ModelAdmin):
	list_display = ('nazwa', 'pozycja_N', 'pozycja_E', 'promien')