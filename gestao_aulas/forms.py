# gestao_aulas/forms.py
from django import forms
from .models import Aluno, Aula
from usuarios.models import Professor


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
            "dia_semana",
            "horario_fixo",
        ]
        widgets = {
            "nome": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome do aluno"}
            ),
            "sobrenome": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Sobrenome do aluno"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "email@exemplo.com"}
            ),
            "telefone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "(11) 99999-9999"}
            ),
            "disciplina": forms.Select(attrs={"class": "form-select"}),
            "horas_contratadas": forms.NumberInput(
                attrs={"class": "form-control", "min": "1", "max": "100", "step": "0.5"}
            ),
            "dia_semana": forms.Select(attrs={"class": "form-select"}),
            "horario_fixo": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["disciplina"].choices = Professor.DISCIPLINA_CHOICES
        self.fields["dia_semana"].choices = Aluno.DIAS_SEMANA_CHOICES


class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ["aluno", "data_aula", "duracao", "assunto"]
        widgets = {
            "aluno": forms.Select(attrs={"class": "form-select"}),
            "data_aula": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "duracao": forms.NumberInput(
                attrs={"class": "form-control", "min": "0.5", "max": "8", "step": "0.5"}
            ),
            "assunto": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        professor = kwargs.pop("professor", None)
        super().__init__(*args, **kwargs)
        if professor:
            self.fields["aluno"].queryset = Aluno.objects.filter(
                professor=professor, ativo=True
            )
