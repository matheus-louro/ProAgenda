# gestao_aulas/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db import models
from django.core.paginator import Paginator
from .models import Aluno, Aula
from .forms import AlunoForm, AulaForm


class ProfessorRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")


class DashboardView(ProfessorRequiredMixin, View):
    template_name = "gestao_aulas/dashboard.html"

    def get_context_data(self, request, form=None, aula_form=None):
        professor = request.user

        alunos_ativos = Aluno.objects.filter(professor=professor, ativo=True).order_by(
            "nome"
        )

        alunos_saldo_baixo = alunos_ativos.filter(saldo_horas__lte=2)

        proximas_aulas = alunos_ativos.filter(dia_semana__isnull=False).order_by(
            "dia_semana"
        )

        aulas_recentes = Aula.objects.filter(aluno__professor=professor).order_by(
            "-data_aula"
        )[:5]

        total_horas_query = Aula.objects.filter(aluno__professor=professor).aggregate(
            total=models.Sum("duracao")
        )
        total_horas = total_horas_query["total"] or 0

        total_horas_formatadas = (
            f"{total_horas:.1f}" if isinstance(total_horas, float) else f"{total_horas}"
        )

        form_instance = form or AlunoForm()
        aula_form_instance = aula_form or AulaForm(professor=professor)

        context = {
            "alunos": alunos_ativos,
            "total_alunos_ativos": alunos_ativos.count(),
            "alunos_saldo_baixo": alunos_saldo_baixo,
            "proximas_aulas": proximas_aulas,
            "today": timezone.now(),
            "form": form_instance,
            "aula_form": aula_form_instance,
            "aulas_recentes": aulas_recentes,
            "total_horas_ministradas": total_horas_formatadas,
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


class MeusAlunosView(ProfessorRequiredMixin, View):
    template_name = "gestao_aulas/meus_alunos.html"

    def get(self, request):
        alunos_list = Aluno.objects.filter(professor=request.user).order_by("nome")

        total_alunos = alunos_list.count()
        alunos_ativos = alunos_list.filter(ativo=True).count()
        alunos_inativos = alunos_list.filter(ativo=False).count()

        total_horas_data = alunos_list.aggregate(total=models.Sum("horas_contratadas"))
        total_horas = total_horas_data["total"] or 0

        disciplinas = alunos_list.values_list("disciplina", flat=True).distinct()

        paginator = Paginator(alunos_list, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "alunos": page_obj,
            "total_alunos": total_alunos,
            "alunos_ativos": alunos_ativos,
            "alunos_inativos": alunos_inativos,
            "total_horas": total_horas,
            "disciplinas": disciplinas,
            "form": AlunoForm(),
            "today": timezone.now(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get("action")

        if action == "add_aluno":
            form = AlunoForm(request.POST)
            if form.is_valid():
                aluno = form.save(commit=False)
                aluno.professor = request.user
                aluno.saldo_horas = aluno.horas_contratadas
                aluno.save()
                return redirect("meus_alunos")
            return self.get(request)

        elif action == "edit_aluno":
            aluno_id = request.POST.get("aluno_id")
            aluno_obj = get_object_or_404(Aluno, pk=aluno_id, professor=request.user)

            horas_antigas = aluno_obj.horas_contratadas

            form = AlunoForm(request.POST, instance=aluno_obj)

            if form.is_valid():
                aluno = form.save(commit=False)
                horas_novas = aluno.horas_contratadas

                if horas_novas > horas_antigas:
                    horas_adicionadas = horas_novas - horas_antigas
                    aluno.saldo_horas += horas_adicionadas

                if aluno.saldo_horas < 0:
                    aluno.saldo_horas = 0

                aluno.save()
                return redirect("meus_alunos")
            return self.get(request)

        elif action == "delete_aluno":
            aluno_id = request.POST.get("aluno_id")
            aluno_obj = get_object_or_404(Aluno, pk=aluno_id, professor=request.user)
            aluno_obj.delete()
            return redirect("meus_alunos")

        elif action == "toggle_status":
            aluno_id = request.POST.get("aluno_id")
            aluno_obj = get_object_or_404(Aluno, pk=aluno_id, professor=request.user)
            aluno_obj.ativo = not aluno_obj.ativo
            aluno_obj.save()
            return redirect("meus_alunos")

        return redirect("meus_alunos")


class HistoricoAlunoView(ProfessorRequiredMixin, View):
    template_name = "gestao_aulas/historico_aluno.html"

    def get(self, request, aluno_id):
        aluno = get_object_or_404(Aluno, pk=aluno_id, professor=request.user)
        aulas = Aula.objects.filter(aluno=aluno).order_by("-data_aula")

        total_aulas = aulas.count()
        total_horas = aulas.aggregate(total=models.Sum("duracao"))["total"] or 0
        horas_restantes = aluno.saldo_horas

        context = {
            "aluno": aluno,
            "aulas": aulas,
            "total_aulas": total_aulas,
            "total_horas": total_horas,
            "horas_restantes": horas_restantes,
            "today": timezone.now(),
        }
        return render(request, self.template_name, context)
