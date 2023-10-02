from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import path

from . import views

app_name = 'lab'

urlpatterns = [
    path('home',  login_required(views.home), name='home'),
    path('cadastro-usuario/', user_passes_test(lambda u: u.is_superuser)
         (login_required(views.cadastro_usuario)), name='cadastro_usuario'),
    # path('cadastro-paciente/', login_required(views.cadastro_paciente),
    # name='cadastro_paciente'),
    path('laudo-consultar/', login_required(views.laudo_consultar),
         name='laudo_consultar'),
    path('laudo-enviar/', login_required(views.laudo_enviar),
         name='laudo_enviar'),
    path('pesquisa/', login_required(views.pesquisa), name='pesquisa'),
    path('alterar-dados', login_required(views.alterar_dados),
         name='alterar_dados')
]
