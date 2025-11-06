from django import forms
from .models import Aluno, Aula


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            "nome",
            "sobrenome",
            "email",
            "telefone",
            "disciplina",
            "horas_contratadas",
        ]


class AulaForm(forms.ModelForm):
    data_aula = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Aula
        fields = ["aluno", "data_aula", "duracao", "assunto"]

    def __init__(self, *args, **kwargs):
        professor = kwargs.pop("professor", None)
        super().__init__(*args, **kwargs)

        if professor:
            self.fields["aluno"].queryset = Aluno.objects.filter(
                professor=professor, ativo=True
            ).order_by("nome")
