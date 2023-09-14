from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'lab/pages/home.html')


def cadastro_paciente(request):
    return render(request, 'lab/pages/cadastro_paciente.html')


def laudo(request):
    return render(request, 'lab/pages/laudo.html')


def laudo_enviar(request):
    return render(request, 'lab/pages/laudo_enviar.html')


def pesquisa(request):
    return render(request, 'lab/pages/pesquisa.html')


def alterar_dados(request):
    return render(request, 'lab/pages/alterar_dados.html')
