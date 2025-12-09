from django import forms
from .models import RegistroSono

class RegistroSonoForm(forms.ModelForm):
    class Meta:
        model = RegistroSono
        fields = [
            'data_dormiu',
            'data_acordou',
        ]
        widgets = {
            'data_dormiu': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_acordou': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
