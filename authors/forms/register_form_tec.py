from authors.models import CustomUser, Tec
from django import forms
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterFormLabTec(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Digite o nome de usuário')
        add_placeholder(self.fields['first_name'], 'Digite o primeiro nome')
        add_placeholder(self.fields['last_name'], 'Digite o sobrenome')
        add_placeholder(self.fields['email'], 'Digite o e-mail')
        add_placeholder(self.fields['crm'], 'Digite o CRM')

    username = forms.CharField(
        error_messages={
            'required': 'Este campo não pode estar vazio',
            'min_length': ('O nome de usuário deve conter '
                           'no mínimo 4 caracteres'),
            'max_length': ('O nome de usuário deve conter '
                           'no máximo 150 caracteres')
        },
        label='Usuário',
        help_text='Obrigatório. '
        '150 caracteres ou menos. '
        'Letras, números e @/./+/-/_ apenas.',
        min_length=4, max_length=150,
    )

    # Nome do usuário
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
        label='Confirmação de senha',
    )

    crm = forms.CharField(
        error_messages={
            'required': 'E-mail é obrigatório'
        },
        label='CRM',
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
            'crm',

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

    def clean_crm(self):
        crm = self.cleaned_data.get('crm', '')
        exists = Tec.objects.filter(crm=crm).exists()

        if exists:
            raise ValidationError(
                'Esse CRM já está em uso', code='invalid',
            )

        return crm

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
            Tec.objects.create(user=user, crm=self.cleaned_data['crm'])
        return user
