import requests
from authors.models import CustomUser, Patient
from django import forms
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterFormPatient(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite o nome de usuário')
        add_placeholder(self.fields['first_name'], 'Digite o primeiro nome')
        add_placeholder(self.fields['last_name'], 'Digite o sobrenome')
        add_placeholder(self.fields['email'], 'Digite o e-mail')
        add_placeholder(self.fields['cpf'], 'Digite o cpf')
        add_placeholder(self.fields['cell'], 'Digite o número telefônico')
        add_placeholder(self.fields['city'], 'Digite o nome da cidade')
        add_placeholder(self.fields['street'], 'Digite o nome da rua')
        add_placeholder(self.fields['number'], 'Digite o número da residência')
        self.fields['state'].choices = self.carregar_estados()

    def carregar_estados(self):
        estados = []
        try:
            response = requests.get(
                'https://servicodados.ibge.gov.br/api/v1/localidades/estados')
            if response.status_code == 200:
                data = response.json()
                for estado in data:
                    estados.append((estado['sigla'], estado['nome']))
        except requests.RequestException as e:
            print('Erro ao carregar estados:', e)
        return estados

    first_name = forms.CharField(
        error_messages={
            'required': 'Este campo não pode estar vazio'
        },
        label='Nome',
        max_length=30,
    )

    # Sobrenome
    last_name = forms.CharField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Sobrenome',
        max_length=30,
    )

    birthday = forms.DateField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Data de nascimento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    # Nome do usuário
    username = forms.CharField(
        error_messages={
            'required': 'Este campo não pode estar vazio',
            'min_length': ('O nome de usuário deve conter '
                           'no mínimo 4 caracteres'),
            'max_length': ('O nome de usuário deve conter '
                           'no máximo 150 caracteres')
        },
        label='Nome do usuário',
        help_text='Obrigatório. '
        '150 caracteres ou menos. '
        'Letras, números e @/./+/-/_ apenas.',
        min_length=4, max_length=150,
    )

    # Email
    email = forms.EmailField(
        error_messages={
            'required': 'E-mail é obrigatório'
        },
        label='E-mail',
        help_text='O e-mail deve ser válido.',
    )

    # Senha principal
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Crie uma senha'
        }),
        error_messages={
            'required': 'A senha não pode estar vazia'
        },
        help_text=(
            'Senha deve ter pelo menos um caracter maiúsculo, '
            'um caracter minúsculo e um número. A senha deve '
            'possuir pelo menos 8 caracteres.'
        ),
        label='Senha',
        validators=[strong_password]
    )

    # Senha confirmacao
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite novamente a senha'
        }),
        error_messages={
            'required': 'A senha não pode estar vazia'
        },
        label='Confirme a senha',
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

    cell = forms.CharField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Telefone',
        max_length=15
    )

    city = forms.ChoiceField(
        choices=[],  # As opções serão preenchidas dinamicamente
        required=False,
        label='Cidade',
        widget=forms.Select(
            attrs={'class': 'city-select-patient', 'id': 'id_city'})
    )

    state = forms.ChoiceField(
        choices=[],  # As opções serão preenchidas dinamicamente
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Estado',
        widget=forms.Select(
            attrs={'class': 'state-select-patient', 'id': 'id_state'})
    )

    cpf = forms.CharField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='CPF',
        max_length=14
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'cpf',
            'birthday',
            'email',
            'password',
            'password2',
            'cell',
            'state',
            'city',
            'street',
            'number',
        ]
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'cpf-mask'})
        }

    # Funcao que levanta erro se for cadastrar com o mesmo email

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:
            raise forms.ValidationError('Por favor, selecione uma cidade.')
        # Adicione qualquer outra validação necessária aqui
        return city

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = CustomUser.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Esse e-mail já está em uso', code='invalid',
            )

        return email

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '')
        exists = Patient.objects.filter(cpf=cpf).exists()

        if exists:
            raise ValidationError(
                'Esse CPF já está em uso', code='invalid',
            )

        return cpf

    # metodo para verificar se os campos de senhas sao iguais

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'As senhas devem ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Patient.objects.create(user=user,
                                   birthday=self.cleaned_data['birthday'],
                                   street=self.cleaned_data['street'],
                                   number=self.cleaned_data['number'],
                                   city=self.cleaned_data['city'],
                                   state=self.cleaned_data['state'],
                                   cpf=self.cleaned_data['cpf'],
                                   cell=self.cleaned_data['cell'],
                                   fk_recpt=self.recpt_instance,)
        return user
