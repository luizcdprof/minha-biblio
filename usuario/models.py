from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Turma(models.Model):
    PERIODO_CHOICES = [
        ('manhã', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
        ('integral', 'Integral'),
    ]
    nome = models.CharField(max_length=3, blank=False, null=False)
    periodo = models.CharField(max_length=10, choices=PERIODO_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    PERFIL_CHOICES = [
        ('bibliotecario', 'Bibliotecário'),
        ('usuario', 'Usuário'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False, related_name='usuario_user_set')
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default='usuario')
    imagem = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    ra = models.CharField(max_length=20, blank=True, null=True)
    turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, blank=True, null=True, related_name='usuario_turma_set')
    telefone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username