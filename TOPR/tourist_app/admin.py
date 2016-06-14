from django.contrib import admin
from .models import Turysta, Grupa

@admin.register(Turysta)
class TurystaAdmin(admin.ModelAdmin):
    list_display = ('numer_telefonu', 'pozycja_N', 'pozycja_E', 'ostatni_ruch')

@admin.register(Grupa)
class GrypaAdmin(admin.ModelAdmin):
    list_display = ('lider', 'nazwa')