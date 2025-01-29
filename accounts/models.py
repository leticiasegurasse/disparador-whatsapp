from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    SETOR_CHOICES = [
        ('administrativo', 'Administrativo'),
        ('financeiro', 'Financeiro'),
        ('vendas', 'Vendas'),
        ('estoque', 'Estoque'),
    ]

    setor = models.CharField(
        max_length=20,
        choices=SETOR_CHOICES,
        default='administrativo',
        verbose_name='Setor'
    )

    api_key = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='API Key'
    )

    instancia = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Instância'
    )

    def __str__(self):
        return self.username
