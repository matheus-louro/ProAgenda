# gestao_aulas/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db import models
from .models import Aluno, Aula
from .forms import AlunoForm, AulaForm


class ProfessorRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")


class DashboardView(ProfessorRequiredMixin, View):
    template_name = "gestao_aulas/dashboard.html"

    def get_context_data(self, request, form=None, aula_form=None):
        alunos_ativos = Aluno.objects.filter(
            professor=request.user, ativo=True
        ).order_by("nome")

        aulas_recentes = Aula.objects.filter(aluno__professor=request.user).order_by(
            "-data_aula"
        )[:5]

        total_horas_query = aulas_recentes.aggregate(total=models.Sum("duracao"))
        total_horas = total_horas_query["total"] or 0

        context = {
            "alunos": alunos_ativos,
            "total_alunos_ativos": alunos_ativos.count(),
            "today": timezone.now(),
            "form": form or AlunoForm(),
            "aula_form": aula_form or AulaForm(professor=request.user),
            "aulas_recentes": aulas_recentes,
            "total_horas_ministradas": f"{total_horas}h",
            "aulas_pendentes": 0,
            "receita_mes": "R$ 0,00",
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")

        form = None
        aula_form = None

        if action == "add_aluno":
            form = AlunoForm(request.POST)
            if form.is_valid():
                aluno = form.save(commit=False)
                aluno.professor = request.user
                aluno.saldo_horas = aluno.horas_contratadas
                aluno.save()
                return redirect("dashboard")

        elif action == "lancar_aula":
            aula_form = AulaForm(request.POST, professor=request.user)
            if aula_form.is_valid():
                aula_form.save()
                return redirect("dashboard")

        context = self.get_context_data(request, form=form, aula_form=aula_form)
        return render(request, self.template_name, context)


class AlunoCreateView(ProfessorRequiredMixin, CreateView):
    model = Aluno
    form_class = AlunoForm
    template_name = "gestao_aulas/aluno_form.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        aluno = form.save(commit=False)
        aluno.professor = self.request.user
        aluno.saldo_horas = form.cleaned_data["horas_contratadas"]
        aluno.save()
        return super().form_valid(form)
