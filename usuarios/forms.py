# usuarios/forms.py (CRIE ESTE ARQUIVO)
from django.contrib.auth.forms import UserCreationForm
from .models import Professor


class ProfessorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Professor
        # Adicione os campos que você quer no formulário de cadastro
        fields = ("first_name", "last_name", "email", "disciplinas", "telefone")
