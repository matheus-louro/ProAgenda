# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Professor


class ProfessorCreationForm(UserCreationForm):
    disciplinas = forms.MultipleChoiceField(
        choices=Professor.DISCIPLINA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Selecione uma ou mais disciplinas",
    )

    class Meta:
        model = Professor
        fields = (
            "first_name",
            "last_name",
            "email",
            "disciplinas",
            "telefone",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"class": "form-control"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control"})
        self.fields["email"].widget.attrs.update({"class": "form-control"})
        self.fields["telefone"].widget.attrs.update({"class": "form-control"})
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

    def clean_disciplinas(self):
        """Converte a lista de disciplinas para string separada por vírgula"""
        disciplinas = self.cleaned_data.get("disciplinas", [])
        if not disciplinas:
            raise forms.ValidationError("Selecione pelo menos uma disciplina.")
        return ",".join(disciplinas)
