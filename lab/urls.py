from django.urls import path

from . import views

app_name = 'lab'

urlpatterns = [
    path('', views.home, name='home'),
    path('lab/cadastro-paciente/', views.cadastro_paciente,
         name='cadastro_paciente'),
    path('lab/laudo/', views.laudo, name='laudo'),
    path('lab/laudo-enviar/', views.laudo_enviar, name='envio_laudo'),
    path('lab/pesquisa/', views.pesquisa, name='pesquisa'),
    path('lab/alterar-dados', views.alterar_dados, name='alterar_dados')
]
