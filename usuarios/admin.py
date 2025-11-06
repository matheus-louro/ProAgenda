# usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Professor


@admin.register(Professor)
class ProfessorAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")

    ordering = ("email",)

    fieldsets = UserAdmin.fieldsets + (
        ("Campos Personalizados", {"fields": ("disciplinas", "telefone")}),
    )
