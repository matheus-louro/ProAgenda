# usuarios/models.py
from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)  # <-- Importe o BaseUserManager


class ProfessorManager(BaseUserManager):
    """
    Gerenciador customizado para o model Professor,
    que usa email como campo de login.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um Professor (usuário) com o email e senha fornecidos.
        """
        if not email:
            raise ValueError("O email é obrigatório")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Criptografa a senha
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e salva um Superusuário (admin) com o email e senha.
        """
        # Define os campos de admin como True
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser deve ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Professor(AbstractUser):

    DISCIPLINA_CHOICES = [
        ("matematica", "Matemática"),
        ("portugues", "Português"),
        ("historia", "História"),
        ("geografia", "Geografia"),
        ("ciencias", "Ciências"),
        ("ingles", "Inglês"),
        ("fisica", "Física"),
        ("quimica", "Química"),
        ("biologia", "Biologia"),
        ("outra", "Outra"),
    ]

    email = models.EmailField(unique=True)
    username = None  # Remove o campo username

    disciplinas = models.CharField(
        max_length=100,
        choices=DISCIPLINA_CHOICES,
        blank=False,
        null=False,
    )
    telefone = models.CharField(max_length=20, blank=False, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]  # Campos pedidos no 'createsuperuser'

    objects = ProfessorManager()

    def __str__(self):
        return self.get_full_name() or self.email

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)
