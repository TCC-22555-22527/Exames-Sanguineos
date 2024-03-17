from django.forms import RegisterFormPatient
from django.test import TestCase


class RegisterFormPatientTestCase(TestCase):
    def test_form_submission(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'cpf': '123.456.789-00',
            'birthday': '1990-01-01',
            'email': 'johndoe@example.com',
            'password': 'Test@1234',
            'password2': 'Test@1234',
            'cell': '(12) 99345-6789',
            'state': 'SP',  # Substitua pelos valores reais
            'city': 'Adamantina',  # Substitua pelos valores reais
            'street': 'Street Name',
            'number': '1293'
        }

        form = RegisterFormPatient(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'cpf': '123.456.789-00',
            'birthday': '1990-01-01',
            'email': 'johndoe@example.com',
            'password': 'Test@1234',
            'password2': 'Test@1234',
            'cell': '(12) 99345-6789',
            'state': 'SP',  # Substitua pelos valores reais
            'city': 'Adamantina',  # Substitua pelos valores reais
            'street': 'Street Name',
            'number': '1293'
        }

        form = RegisterFormPatient(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertIsNotNone(user)
