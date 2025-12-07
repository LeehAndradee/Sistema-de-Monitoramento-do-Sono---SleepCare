from django.db import models
from django.contrib.auth.models import User

class RegistroSono(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    data_dormiu = models.DateTimeField()
    data_acordou = models.DateTimeField()

    QUALIDADE_CHOICES = [
        (1, "Muito ruim"),
        (2, "Ruim"),
        (3, "Regular"),
        (4, "Boa"),
        (5, "Excelente"),
    ]
    qualidade = models.IntegerField(choices=QUALIDADE_CHOICES)

    COMO_ACORDOU_CHOICES = [
        ("cansado", "Cansado"),
        ("ok", "Normal"),
        ("bem", "Bem disposto"),
    ]
    como_acordou = models.CharField(max_length=20, choices=COMO_ACORDOU_CHOICES)

    notas_noite = models.TextField(blank=True)

    exercicio_fisico = models.BooleanField(default=False)
    alcool = models.BooleanField(default=False)
    cafeina = models.BooleanField(default=False)
    jantar_tarde = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)
