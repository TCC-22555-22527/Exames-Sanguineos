from authors.models import CustomUser, Patient
from django import forms
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterFormPatient(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite seu nome de usuário')
        add_placeholder(self.fields['first_name'], 'Digite seu primeiro nome')
        add_placeholder(self.fields['last_name'], 'Digite seu sobrenome')
        add_placeholder(self.fields['email'], 'Digite seu e-mail')

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

    birthday = forms.DateField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Data de nascimento',
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
            'placeholder': 'Sua senha'
        }),
        error_messages={
            'required': 'A senha não pode estar vazia'
        },
        help_text=(
            'Senha deve ter pelo menos um caracter maiúsculo, '
            'um caracter minúsculo e um número. A senha deve '
            'possuir pelo menos 8 caracteres.'
        ),
        label='Digite sua senha',
        validators=[strong_password]
    )

    # Senha confirmacao
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite novamente sua senha'
        }),
        error_messages={
            'required': 'A senha não pode estar vazia'
        },
        label='Confirme sua senha',
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

    STATES_CHOICE = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')
    )
    state = forms.ChoiceField(
        choices=STATES_CHOICE,
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='Estado',
        widget=forms.Select(attrs={'class': 'state-select-patient'})
    )

    cpf = forms.CharField(
        error_messages={'required': 'Este campo não pode estar vazio'},
        label='CPF',
        max_length=16
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'username',
            'email',
            'password',
            'password2',
            'street',
            'number',
            'city',
            'state',
            'cpf'
        ]

    # Funcao que levanta erro se for cadastrar com o mesmo email

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
        user.is_tec = True
        if commit:
            user.save()
            Patient.objects.create(user=user,
                                   birthday=self.cleaned_data['birthday'],
                                   street=self.cleaned_data['street'],
                                   number=self.cleaned_data['number'],
                                   city=self.cleaned_data['city'],
                                   state=self.cleaned_data['state'],
                                   cpf=self.cleaned_data['cpf'],
                                   fk_recpt=self.recpt_instance,)
        return user
