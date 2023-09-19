from authors.forms import AuthorReportForm
from django.contrib import messages
from django.shortcuts import redirect, render


# Create your views here.
def home(request):
    return render(request, 'lab/pages/home.html')


def cadastro_paciente(request):
    return render(request, 'lab/pages/cadastro_paciente.html')


def laudo_consultar(request):
    return render(request, 'lab/pages/laudo_consultar.html')


# Dashboard para enviar imagem com dados adicionais
def laudo_enviar(request):
    form = AuthorReportForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            lab = form.save(commit=False)
            lab.save()
            messages.success(request, 'Sua imagem foi salva com sucesso!')

            return redirect('lab:laudo_enviar')

    return render(request, 'lab/pages/laudo_enviar.html',
                  {'form': form}
                  )


def pesquisa(request):
    return render(request, 'lab/pages/pesquisa.html')


def alterar_dados(request):
    return render(request, 'lab/pages/alterar_dados.html')
