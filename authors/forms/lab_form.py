from django import forms
from lab.models import Lab


class AuthorReportForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ['image']
        labels = {
            'image': 'Imagem',
        }
