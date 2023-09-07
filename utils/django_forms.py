import re

from django.core.exceptions import ValidationError


# funcao para modificar algum atributo
def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


# funcao para adicionar placeholder
def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


# criação de senha forte
def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'A senha deve ter no mínimo uma letra maiúscula, '
            'Uma letra minúscula e um número. A senha deve '
            'possuir pelo menos 8 caracteres.'
        ),
            code='invalid'
        )
