from django.conf import settings
from django.db import models

class DisparoHistorico(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="historico_disparos")
    numero = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    mensagem = models.TextField()
    status = models.CharField(max_length=20)  # Ex.: "success" ou "error"
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Disparo para {self.nome} ({self.numero}) por {self.usuario.username}"
