from django.urls import path
from gestao_aulas.views import DashboardView, HistoricoAlunoView, MeusAlunosView


urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("meus_alunos/", MeusAlunosView.as_view(), name="meus_alunos"),
    path(
        "historico/<int:aluno_id>/",
        HistoricoAlunoView.as_view(),
        name="historico_aluno",
    ),
]
