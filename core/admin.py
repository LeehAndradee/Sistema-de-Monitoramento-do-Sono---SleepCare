from django.contrib import admin
from .models import RegistroSono

@admin.register(RegistroSono)
class RegistroSonoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_dormiu', 'data_acordou', 'qualidade', 'total_horas', 'alerta_saude')
    list_filter = ('qualidade', 'usuario')
    search_fields = ('usuario__username',)