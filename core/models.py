from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

QUALIDADE_CHOICES = (
    (1, 'Ruim (Péssimo)'),
    (2, 'Abaixo da Média'),
    (3, 'Médio (Razoável)'),
    (4, 'Bom'),
    (5, 'Excelente (Revigorante)'),
)

class RegistroSono(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registros_sono'
    )
    data_dormiu = models.DateTimeField(verbose_name="Data e Hora que deitou")
    data_acordou = models.DateTimeField(verbose_name="Data e Hora que acordou")
    total_horas_dormidas = models.FloatField(default=0.0, verbose_name="Total de Horas Dormidas (Calculado)")
    qualidade_sono = models.IntegerField(choices=QUALIDADE_CHOICES)
    criado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Registro de Sono"
        verbose_name_plural = "Registros de Sono"
        ordering = ['-data_dormiu']

    def __str__(self):
        return f"Registro de {self.usuario.username} em {self.data_dormiu.strftime('%d/%b/%Y')}"
