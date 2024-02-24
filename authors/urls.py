from django.contrib.auth.decorators import user_passes_test
from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path(
        '',
        views.login_view,
        name='login'
    ),
    path(
        'auth/my-profile/',
        views.my_profile,
        name='my_profile',
    ),
    path(
        'login/create/',
        views.login_create,
        name='login_create',
    ),
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
    # registro de tecnico
    path(
        'auth/register-tec/',
        user_passes_test(lambda u: u.is_superuser)
        (views.register_tec_view),
        name='register_tec'
    ),
    path(
        'register-tec/create/',
        views.register_tec_create,
        name='register_tec_create'
    ),
    # registro de rececpcao
    path(
        'auth/register-recpt/',
        user_passes_test(lambda u: u.is_superuser)
        (views.register_recpt_view),
        name='register_recpt'
    ),
    path(
        'register-recpt/create/',
        views.register_recpt_create,
        name='register_recpt_create'
    ),
    # registro de paciente
    path(
        'auth/register-patient/',
        views.register_patient_view,
        name='register_patient'
    ),
    path(
        'register-patient/create/',
        views.register_patient_create,
        name='register_patient_create'
    ),
]
