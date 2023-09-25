from authors.forms import AuthorReportForm
from django.contrib import messages
from django.shortcuts import redirect, render
from rolepermissions.decorators import has_permission_decorator


# funcao específica do superusuário
def cadastro_usuario(request):
    return render(request, 'lab/pages/cadastro_usuario.html')


# funções de usuários comuns
def home(request):
    return render(request, 'lab/pages/home.html')


@has_permission_decorator('cadastrar_paciente')
def cadastro_paciente(request):
    return render(request, 'lab/pages/cadastro_paciente.html')


@has_permission_decorator('visualizar_laudo')
def laudo_consultar(request):
    return render(request, 'lab/pages/laudo_consultar.html')


# Dashboard para enviar imagem com dados adicionais
@has_permission_decorator('laudo_enviar_permission')
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


@has_permission_decorator('pesquisar_paciente')
def pesquisa(request):
    return render(request, 'lab/pages/pesquisa.html')


@has_permission_decorator('alterar_dados')
def alterar_dados(request):
    return render(request, 'lab/pages/alterar_dados.html')
