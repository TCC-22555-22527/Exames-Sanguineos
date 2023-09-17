from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'lab'

urlpatterns = [
    path('home', views.home, name='home'),
    path('lab/cadastro-paciente/',
         login_required(views.cadastro_paciente), name='cadastro_paciente'),
    path('lab/laudo/', login_required(views.laudo), name='laudo'),
    path('lab/laudo-enviar/', login_required(views.laudo_enviar),
         name='envio_laudo'),
    path('lab/pesquisa/', login_required(views.pesquisa), name='pesquisa'),
    path('lab/alterar-dados', login_required(views.alterar_dados),
         name='alterar_dados')
]
