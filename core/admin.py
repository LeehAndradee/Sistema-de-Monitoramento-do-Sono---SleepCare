from django.contrib import admin
from .models import RegistroSono # Importando o modelo RegistroSono

@admin.register(RegistroSono)
class RegistroSonoAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na tabela da lista de registros
    list_display = (
        'usuario', 
        'data_dormiu', 
        'data_acordou', 
        'qualidade', 
        'total_horas' # Este campo é a propriedade calculada (tempo total de sono)
    )
    
    # Adiciona filtros laterais (Filtrar por qualidade)
    list_filter = ('qualidade',)
    
    # Adiciona barra de busca
    search_fields = ('usuario__username', 'qualidade') # Permite buscar pelo nome do usuário