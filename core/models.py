from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin # <--- ADICIONE ESTA LINHA!

class RegistroSono(models.Model):
    OPCOES_QUALIDADE = [
        ('ruim', 'Ruim'),
        ('medio', 'Médio'),
        ('bom', 'Bom'),
        ('excelente', 'Excelente'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_dormiu = models.DateTimeField(verbose_name="Horário que foi dormir")
    data_acordou = models.DateTimeField(verbose_name="Horário que acordou")
    qualidade = models.CharField(
        max_length=20, 
        choices=OPCOES_QUALIDADE,
        verbose_name="Qualidade do Sono"
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Sono"
        verbose_name_plural = "Registros de Sono"
        ordering = ['-data_dormiu']

    def __str__(self):
        return f"{self.usuario.username} - {self.data_dormiu.strftime('%d/%m/%Y')}"

    # Calcula as horas automaticamente [cite: 20]
    @property
    def total_horas(self):
        diferenca = self.data_acordou - self.data_dormiu
        if diferenca.total_seconds() < 0:
            return 0.0
        horas = diferenca.total_seconds() / 3600
        return round(horas, 2)

   # ... (código do total_horas)

    # --- LÓGICA DE ALERTAS ---
    # Removido o @property
    def alerta_saude(self): 
        if self.total_horas < 7:
            return "⚠️ Você dormiu menos do que o recomendado"
        elif self.total_horas > 12:
            return "❓ Atenção: Verifique as datas (Muitas horas)"
        else:
            return "✅ Seu sono está adequado"

    # Adicionando atributos de Admin para o método
    alerta_saude.short_description = "Alerta de Saúde"
    