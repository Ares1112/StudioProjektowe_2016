from django.contrib import admin
from .models import Turysta, Grupa, Niedzwiedz

@admin.register(Turysta)
class TurystaAdmin(admin.ModelAdmin):
    list_display = ('numer_telefonu', 'pozycja_N', 'pozycja_E', 'ostatni_ruch')

@admin.register(Grupa)
class GrupaAdmin(admin.ModelAdmin):
    list_display = ('lider', 'nazwa')
    
@admin.register(Niedzwiedz)
class NiedzwiedzAdmin(admin.ModelAdmin):
    list_display = ('identyfikator', 'pozycja_N', 'pozycja_E')