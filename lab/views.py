from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'lab/pages/home.html')


def cadastro(request):
    return render(request, 'cadastro.html')


def cadastro_paciente(request):
    return render(request, 'cadastro_paciente.html')


def login(request):
    return render(request, 'login.html')


def laudo(request):
    return render(request, 'laudo.html')


def laudo_enviar(request):
    return render(request, 'laudo_enviar.html')
