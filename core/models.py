from django.db import models
from django.contrib.auth.models import User

class RegistroSono(models.Model):
    OPCOES_QUALIDADE = [
        ('ruim', 'Ruim'),
        ('medio', 'Médio'),
        ('bom', 'Bom'),
        ('excelente', 'Excelente'),
    ]

    # Vínculo com o usuário (quem dormiu?)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Horários
    data_dormiu = models.DateTimeField(verbose_name="Horário que foi dormir")
    data_acordou = models.DateTimeField(verbose_name="Horário que acordou")
    
    # Avaliação
    qualidade = models.CharField(
        max_length=20, 
        choices=OPCOES_QUALIDADE,
        verbose_name="Qualidade do Sono"
    )

    # Data de criação do registro (controle interno)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Sono"
        verbose_name_plural = "Registros de Sono"
        ordering = ['-data_dormiu'] # Mostra os mais recentes primeiro

    def __str__(self):
        return f"{self.usuario.username} - {self.data_dormiu.strftime('%d/%m/%Y')}"

    # Método para calcular horas dormidas automaticamente [cite: 14, 20]
    @property
    def total_horas(self):
        diferenca = self.data_acordou - self.data_dormiu
        # Converte segundos para horas
        horas = diferenca.total_seconds() / 3600
        return round(horas, 2)