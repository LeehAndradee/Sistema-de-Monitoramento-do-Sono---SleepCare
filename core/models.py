from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RegistroSono(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros_sono')
    data_dormiu = models.DateTimeField()
    data_acordou = models.DateTimeField()
    total_horas_dormidas = models.FloatField(default=0.0)
    criado_em = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        diferenca = self.data_acordou - self.data_dormiu
        self.total_horas_dormidas = round(diferenca.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Registro de {self.usuario.username} em {self.data_dormiu.strftime('%d/%b/%Y')}"
