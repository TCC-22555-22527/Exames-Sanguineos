

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from lab.models import DetectedImage, Lab
from project.roles import PatientUser, RecptUSer, TecUser
from rolepermissions.decorators import has_permission_decorator
from rolepermissions.roles import assign_role

from .forms import (LoginForm, RegisterFormLabTec, RegisterFormPatient,
                    RegisterFormReception)
from .models import Patient, Recpt, Tec


@login_required(login_url='authors:login', redirect_field_name='next')
def my_profile(request):

    if request.user.is_superuser:
        adm_instance = request.user.is_superuser
        recpts = Recpt.objects.all()
        tecs = Tec.objects.all()
        return render(request, 'authors/pages/my_profile.html', {
            'adm': adm_instance,
            'recpts': recpts,
            'tecs': tecs,
        })
    else:
        try:
            recpt_instance = request.user.recpt_profile
            patients = Patient.objects.filter(fk_recpt=recpt_instance)
            return render(request, 'authors/pages/my_profile.html', {
                'patients': patients,
                'recpt': recpt_instance,
            })
        except Recpt.DoesNotExist:
            pass

        try:
            tec_instance = request.user.tec_profile
            labs = Lab.objects.filter(fk_tec=tec_instance)
            return render(request, 'authors/pages/my_profile.html', {
                'labs': labs,
                'tec': tec_instance,
            })
        except Tec.DoesNotExist:
            pass

        try:
            patient_instance = request.user.patient_profile
            lab_instances = Lab.objects.filter(patient=patient_instance)
            detected_images = DetectedImage.objects.filter(
                lab__in=lab_instances)
            return render(request, 'authors/pages/my_profile.html', {
                'patient': patient_instance,
                'reports': detected_images,
                'lab': lab_instances,

            })
        except Patient.DoesNotExist:
            pass


# funcao de login
def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


# funcao pos login
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
            login(request, authenticated_user)
            return redirect(login_to_home)
        else:
            messages.error(request, 'Credenciais inválidas')
    else:
        messages.error(request, 'Nome de usuário e senha inválidos')

    return redirect('authors:login')


# logout
@ login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))


# TEC
@ login_required(login_url='authors:login', redirect_field_name='next')
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


def register_tec_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterFormLabTec(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.is_tec_user = True
        user.save()

        tec = Tec(
            user=user,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            crm=form.cleaned_data['crm'],
            crm_state=form.cleaned_data['crm_state']
        )
        tec.save()

        assign_role(user, TecUser)

        messages.success(
            request, 'O usuário com função de técnico está criado'
        )

        del (request.session['register_form_data'])
        return redirect(reverse('lab:register_custom_user'), {
        })

    del (request.session['register_form_data'])
    return redirect('authors:register_tec')


# RECEPTION
@ login_required(login_url='authors:login', redirect_field_name='next')
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


def register_recpt_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterFormReception(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.is_recpt_user = True
        user.save()

        recpt = Recpt(
            user=user,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
        )
        recpt.save()

        assign_role(user, RecptUSer)

        messages.success(
            request, 'O usuário com função de recepcionista está criado'
        )

        del (request.session['register_form_data'])
        return redirect(reverse('lab:register_custom_user'))

    del (request.session['register_form_data'])
    return redirect('authors:register_recpt')


# PATIENT
@login_required(login_url='authors:login', redirect_field_name='next')
@ has_permission_decorator('cadastrar_paciente')
def register_patient_view(request):
    is_patient_registration_page = request.path == reverse(
        'authors:register_patient')

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterFormPatient(register_form_data)
    return render(request, 'authors/pages/register_view_patient.html', {
        'form': form,
        'form_action': reverse('authors:register_patient_create'),
        'is_patient_registration': is_patient_registration_page
    })


@ has_permission_decorator('cadastrar_paciente')
def register_patient_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST

    form = RegisterFormPatient(POST)
    print(f'usuario logado: {request.user}')

    id_city = request.POST.get('city')
    form.fields['city'].choices = [(id_city, id_city)]
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.is_patient_user = True
        user.save()

        if request.user.is_superuser:
            patient = Patient(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                birthday=form.cleaned_data['birthday'],
                street=form.cleaned_data['street'],
                number=form.cleaned_data['number'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                cpf=form.cleaned_data['cpf'],
                cell=form.cleaned_data['cell'],
                fk_recpt=None,
            )
            patient.save()
        elif request.user.recpt_profile:
            recpt_instance = Recpt.objects.get(user=request.user)
            print(f' instancia de recpt: {recpt_instance}')

            patient = Patient(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                birthday=form.cleaned_data['birthday'],
                street=form.cleaned_data['street'],
                number=form.cleaned_data['number'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                cpf=form.cleaned_data['cpf'],
                fk_recpt=recpt_instance,
                cell=form.cleaned_data['cell'],
            )
            patient.save()

        assign_role(user, PatientUser)

        messages.success(
            request, 'O usuário com função de paciente está criado'
        )

        del (request.session['register_form_data'])
        return redirect(reverse('authors:register_patient'))
    else:
        print(form.errors)
        messages.error(
            request, 'Deu ruim'
        )

    del (request.session['register_form_data'])
    return redirect('authors:register_patient')
