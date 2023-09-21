from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (LoginForm, RegisterForm, RegisterFormLabTec,
                    RegisterFormPatient, RegisterFormReception)


# funcao de cadastro
def register_view(request):
    is_registration_page = request.path == reverse('authors:register')

    # URL de redirecionamento para a página de login
    back_url = reverse('authors:login')

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
        'is_registration_page': is_registration_page,
        'back_url': back_url,
    })


# funcao de pos cadastro
def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(
            request, 'Seu usuário foi criado, por favor, inicia a sessão.')

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')

# funcao de login


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login_temp.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
    })

# funcao pos login

# verifica se esta autenticado e loga ele, lancando msg


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_to_home = reverse('lab:home')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            # messages.success(request, 'Você está logado')
            login(request, authenticated_user)
            return redirect(login_to_home)
        else:
            messages.error(request, 'Credenciais inválidas')
    else:
        messages.error(request, 'Nome de usuário e senha inválidos')

    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))


# vou ter que criar funcoes para cada tipo de funcionario de  - VIEW
def register_tec_view(request):
    is_lab_tec_registration_page = request.path == reverse(
        'authors:register_tec')

    back_url = reverse('lab:home')
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterFormLabTec(register_form_data)

    return render(request, 'authors/pages/register_view_tec.html', {
        'form': form,
        'form_action': reverse('authors:register_tec_create'),
        'is_lab_tec_registration': is_lab_tec_registration_page,
        'back_url': back_url,
    })


# tec CREATE
def register_tec_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterFormLabTec(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(
            request, 'O usuário com função de técnico está criado'
        )

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register_tec')


def register_recpt_view(request):
    is_recpt_registration_page = request.path == reverse(
        'authors:register_recpt')

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterFormReception(register_form_data)
    return render(request, 'authors/pages/register_view_recpt.html', {
        'form': form,
        'form_action': reverse('authors:register_recpt_create'),
        'is_recpt_registration': is_recpt_registration_page
    })


def register_patient_view(request):
    is_patient_registration_page = request.path == reverse(
        'authors:register_patient')

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterFormPatient(register_form_data)
    return render(request, 'authors/pages/register_view_patient.html', {
        'form': form,
        'form_action': reverse('authors:register_patient_create'),
        'is_recpt_registration': is_patient_registration_page
    })


# vou ter que criar funcoes para cada tipo de funcionario de - CREATE


def register_recpt_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterFormReception(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(
            request, 'O usuário com função de recepcionista está criado'
        )

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register_recpt')


def register_patient_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterFormPatient(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(
            request, 'O usuário com função de paciente está criado'
        )

        del (request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register_patient')
