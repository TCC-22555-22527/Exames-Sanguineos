from django import forms
from lab.models import Lab


class AuthorReportForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ['name', 'cpf', 'image']
        labels = {
            'name': 'Nome do paciente',
            'cpf': 'CPF do paciente',
            'image': 'Imagem',
        }
