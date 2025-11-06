from django.urls import path
from gestao_aulas.views import AlunoCreateView, DashboardView


urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("aluno/novo/", AlunoCreateView.as_view(), name="aluno_create"),
]
