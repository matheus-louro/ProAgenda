# gestao_aulas/models.py
from django.db import models
from django.conf import (
    settings,
)
from usuarios.models import Professor


class Aluno(models.Model):
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="alunos",
    )

    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True)

    disciplina = models.CharField(max_length=100, choices=Professor.DISCIPLINA_CHOICES)

    horas_contratadas = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    saldo_horas = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome}"

    # Garante que o saldo inicial seja igual ao contratado ao criar
    def save(self, *args, **kwargs):
        if self.pk is None and self.saldo_horas == 0.0:
            self.saldo_horas = self.horas_contratadas
        super().save(*args, **kwargs)


class Aula(models.Model):
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name="aulas",
    )
    data_aula = models.DateField()
    duracao = models.DecimalField(max_digits=4, decimal_places=2)
    assunto = models.TextField(blank=True, null=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Aula de {self.aluno} em {self.data_aula}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.aluno.saldo_horas -= self.duracao
            self.aluno.save()
        super().save(*args, **kwargs)
