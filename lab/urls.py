from django.contrib import admin
from django.urls import path

from lab import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('cadastro/', views.cadastro),
    path('cadastro-paciente/', views.cadastro_paciente),
    path('laudo/', views.laudo),
    path('laudo-enviar/', views.laudo_enviar),
    path('login/', views.login),
]
