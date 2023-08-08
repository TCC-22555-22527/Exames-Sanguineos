from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return HttpResponse('HOME')


def cadastro(request):
    return HttpResponse('CADASTRO')


def cadastro_paciente(request):
    return HttpResponse('CADASTRO PACIENTE')


def login(request):
    return HttpResponse('LOGIN')


def laudo(request):
    return HttpResponse('LAUDO')


def laudo_enviar(request):
    return HttpResponse('LAUDO PESQUISAR')
