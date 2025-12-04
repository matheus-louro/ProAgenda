from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


class ProfessorManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
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
    username = None


    disciplinas = models.CharField(
        max_length=255,  
        blank=False,
        null=False,
        help_text="Separe as disciplinas por vírgula",
    )
    telefone = models.CharField(max_length=20, blank=False, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = ProfessorManager()

    def __str__(self):
        return self.get_full_name() or self.email

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        super().save(*args, **kwargs)

    def get_disciplinas_list(self):
        """Retorna uma lista das disciplinas"""
        if not self.disciplinas:
            return []
        # Remove espaços e divide por vírgula
        return [d.strip() for d in self.disciplinas.split(",")]

    def get_disciplinas_display(self):
        """Retorna as disciplinas formatadas para exibição"""
        disciplinas_list = self.get_disciplinas_list()

        # Mapeia códigos para nomes amigáveis
        disciplina_map = dict(self.DISCIPLINA_CHOICES)

        disciplinas_display = []
        for codigo in disciplinas_list:
            if codigo in disciplina_map:
                disciplinas_display.append(disciplina_map[codigo])
            else:
                disciplinas_display.append(codigo)

        return ", ".join(disciplinas_display)
