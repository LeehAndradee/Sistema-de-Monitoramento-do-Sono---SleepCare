from django.contrib import admin
from .models import RegistroSono

@admin.register(RegistroSono)
class RegistroSonoAdmin(admin.ModelAdmin):
    # A ÚNICA LINHA QUE VOCÊ PRECISA CONFERIR
    list_display = (
        'usuario', 
        'data_dormiu', 
        'qualidade', 
        'total_horas', 
        'alerta_saude' # <--- ESTE CAMPO DEVE ESTAR AQUI!
    )
    list_filter = ('qualidade',)
    search_fields = ('usuario__username', 'qualidade')

    