from django import forms
from .models import RegistroSono

class RegistroSonoForm(forms.ModelForm):
    class Meta:
        model = RegistroSono
        fields = [
            'data_dormiu', 'data_acordou',
            'qualidade', 'como_acordou',
            'notas_noite',
            'exercicio_fisico', 'alcool',
            'cafeina', 'jantar_tarde'
        ]
        widgets = {
            'data_dormiu': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_acordou': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notas_noite': forms.Textarea(attrs={'rows': 3}),
        }
