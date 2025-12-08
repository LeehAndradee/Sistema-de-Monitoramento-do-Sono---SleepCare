from django.contrib import admin
from .models import RegistroSono

@admin.register(RegistroSono)
class RegistroSonoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "data_dormiu", "data_acordou", "qualidade_sono", "mostrar_total_horas")
    

    @admin.display(description="Total de Horas")
    def mostrar_total_horas(self, obj):
        return obj.total_horas_dormidas