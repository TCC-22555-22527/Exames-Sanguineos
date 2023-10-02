import os

from authors.forms import AuthorReportForm
from authors.forms.register_form_patient import RegisterFormPatient
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from rolepermissions.decorators import has_permission_decorator
from utils.pagination import make_pagination

# vou precisar import
PER_PAGE = os.environ.get('PER_PAGE', 6)

# funcao específica do superusuário


def cadastro_usuario(request):
    return render(request, 'lab/pages/cadastro_usuario.html')


# funções de usuários comuns
def home(request):
    return render(request, 'lab/pages/home.html')

# isso acho que nao vou usar
# @has_permission_decorator('cadastrar_paciente')
# def cadastro_paciente(request):
# return render(request, 'lab/pages/cadastro_paciente.html')


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
    search_term = request.GET.get('q', '').strip()

    patients = []

    if search_term:
        patients = RegisterFormPatient.Meta.model.objects.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(cpf__icontains=search_term)
        ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request, patients, PER_PAGE)

    return render(request, 'lab/pages/pesquisa.html', {
        'page_title': f'Pesquisar por "{search_term}" |',
        'search_term': search_term,
        'patients': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })


@has_permission_decorator('alterar_dados')
def alterar_dados(request):
    return render(request, 'lab/pages/alterar_dados.html')
