from django import forms
from lab.models import BackupImage


class AuthorReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = BackupImage
        fields = 'image',

        widgets = {
            'image': forms.FileInput()
        }
        labels = {
            'image': 'Imagem',
        }
