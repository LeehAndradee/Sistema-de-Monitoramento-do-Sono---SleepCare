# core/forms.py (AJUSTADO)
from django import forms
from .models import RegistroSono

class RegistroSonoForm(forms.ModelForm):
    class Meta:
        model = RegistroSono
        # Campos que o formulário deve exibir
        fields = ('data_dormiu', 'hora_acordou', 'qualidade_sono')

        # Configurações visuais dos campos (Melhor UX)
        widgets = {
            # O 'datetime-local' é ideal para capturar data E hora no mesmo campo
            'data_dormiu': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'hora_acordou': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            # 'qualidade_sono' (select)
        }