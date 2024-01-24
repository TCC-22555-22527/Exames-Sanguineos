from django import forms


class SearchReportForm(forms.Form):
    text = forms.CharField(max_length=50, required=False,
                           label='Filtre por nome ou CPF')
    data = forms.DateField(required=False, widget=forms.TextInput(
        attrs={'type': 'date'}), label='Pesquisar por Data')
