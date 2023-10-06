import os

from authors.forms import AuthorReportForm, EditProfileForm
from authors.models import Patient
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from rolepermissions.decorators import has_permission_decorator
from utils.pagination import make_pagination

from .models import Lab

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
    form = AuthorReportForm()
    selected_patient = None

    if request.method == 'POST':
        image = request.FILES.get('image')
        selected_patient_id = request.POST.get('selected_patient')

        if selected_patient_id and image:
            try:
                selected_patient = Patient.objects.get(id=selected_patient_id)

                lab = Lab(patient=selected_patient,
                          name=selected_patient.first_name,
                          cpf=selected_patient.cpf,
                          image=image)
                lab.save()

                messages.success(request, 'Sua imagem foi salva com sucesso!')
            except Patient.DoesNotExist:
                messages.error(request, 'Paciente não encontrado.')
        else:
            messages.error(
                request, 'Preencha todos os campos antes de enviar.')

        return redirect('lab:laudo_enviar')

    patients = Patient.objects.all()

    if request.method == 'GET' and 'q' in request.GET:
        search_term = request.GET['q'].strip()
        patients = Patient.objects.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(cpf__icontains=search_term)
        )

    return render(request, 'lab/pages/laudo_enviar.html',
                  {'patients': patients,
                   'form': form,
                   'selected_patient': selected_patient})


@has_permission_decorator('pesquisar_paciente')
def pesquisa(request):
    search_term = request.GET.get('q', '').strip()

    patients = []

    if search_term:
        patients = Patient.objects.filter(
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
def usuario_detalhes(request, usuario_id):
    user = get_object_or_404(Patient, pk=usuario_id)
    # Substitua "Patient" pelo seu modelo de usuário
    return render(request, 'lab/pages/usuario_detalhes.html', {'user': user})


# NAO ESTA SENDO USADO
# @has_permission_decorator('alterar_dados')
# def editar_perfil(request, usuario_id):
#    user = get_object_or_404(CustomUser, pk=usuario_id)

#   return render(request, 'lab/pages/alterar_dados.html', {'user': user})


@has_permission_decorator('alterar_dados')
def alterar_dados(request, usuario_id):
    user = get_object_or_404(Patient, pk=usuario_id)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)  # Corrigido aqui
        if form.is_valid():
            form.save()
            # Redirecionar para a página de perfil após a edição
            return redirect('lab:usuario_detalhes', usuario_id=usuario_id)
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'lab/pages/alterar_dados.html', {
        'user': user, 'form': form})
