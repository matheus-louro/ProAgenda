from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from usuarios.forms import ProfessorCreationForm


class CadastroView(CreateView):
    form_class = ProfessorCreationForm
    success_url = reverse_lazy("login")
    template_name = "usuarios/cadastro.html"
