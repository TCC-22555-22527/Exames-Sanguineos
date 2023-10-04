from authors.models import CustomUser
from django import forms
from utils.django_forms import add_placeholder


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Digite o novo nome')
        add_placeholder(self.fields['last_name'], 'Digite o novo sobrenome')
        add_placeholder(self.fields['cpf'], 'Digite o novo CPF')
        add_placeholder(self.fields['birthday'],
                        'Digite a nova data de aniversário')
        add_placeholder(self.fields['street'], 'Digite o novo nome de rua')
        add_placeholder(self.fields['number'],
                        'Digite o novo número residencial')
        add_placeholder(self.fields['city'], 'Digite a nova cidade')
        add_placeholder(self.fields['state'], 'Digite o novo estado')

    first_name = forms.CharField(
        error_messages={
            'required': 'Este campo não pode estar vazio'
        },
        label='Nome'
    )
    # Sobrenome
    last_name = forms.CharField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Sobrenome'
    )
    cpf = forms.CharField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='CPF',
        max_length=16
    )
    birthday = forms.DateField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Data de nascimento'
    )
    street = forms.CharField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Rua',
        max_length=65
    )
    number = forms.IntegerField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Número da residência'
    )
    city = forms.CharField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Cidade',
        max_length=50
    )
    state = forms.CharField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Estado',
        max_length=50
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'cpf',
                  'birthday', 'street', 'number', 'city', 'state']
