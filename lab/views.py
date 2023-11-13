import os
import re
import shutil
import subprocess

from authors.forms import AuthorReportForm, EditProfileForm
from authors.models import Patient
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.core.files import File
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from rolepermissions.decorators import has_permission_decorator
from utils.pagination import make_pagination

from .models import DetectedImage, Lab

# from yolov5.Inference_files.detect import detect


# vou precisar import
PER_PAGE = os.environ.get('PER_PAGE', 6)


# funcao específica do superusuário
def cadastro_usuario(request):
    return render(request, 'lab/pages/cadastro_usuario.html')


# funções de usuários comuns
def home(request):
    return render(request, 'lab/pages/home.html')


# @has_permission_decorator('laudo_enviar_permission')
def laudo_enviar(request):
    form = AuthorReportForm()
    selected_patient = None
    detected_objects = None

    total_rbc = 0
    total_wbc = 0
    total_plaquetas = 0

    if request.method == 'POST':
        # captura a imagem enviada no form
        image = request.FILES.get('image')
        # captura o paciente selecionado
        selected_patient_id = request.POST.get('selected_patient')

        # caso os valores sejam verdadeiros
        if selected_patient_id and image:
            try:
                # obtem o id do paciente selecionado
                selected_patient = Patient.objects.get(id=selected_patient_id)
                # salva a imagem e os dados do paciente no bd
                lab = Lab(patient=selected_patient,
                          name=selected_patient.first_name,
                          cpf=selected_patient.cpf,
                          image=image)
                lab.save()

                # Defina o caminho do arquivo de saída que vai ter rbc, etc.
                output_file_path = "output.txt"

                # Obtem o caminho da imagem que foi enviada e salva
                image_path = os.path.join('media/' + lab.image.name)
                # comando para detectar objetos na imagem
                detect_command = (
                    "python yolov5/Inference_files/detect.py "
                    f"--source {image_path} "
                    "--weights yolov5/Inference_files/best_BCCM.pt "
                    "--output lab_results/"
                )

                # Execute o comando e redirecione a saída para o arquivo
                with open(output_file_path, "w") as output_file:
                    subprocess.run(detect_command, shell=True,
                                   stdout=output_file)

                # Leia a saída do arquivo após o término do processo
                with open(output_file_path, "r") as output_file:
                    output_content = output_file.read()
                    print(
                        f"Output Content: {output_content}" + "fim da variável")  # noqa: E501

                # Agora, você pode processar 'output_content' para extrair
                matches = re.findall(r'(\d+)\s+(RBC|WBC|Platelets)', output_content)  # noqa: E501
                print(f"Matches: {matches}")

                if matches:
                    # Iterar sobre as correspondências
                    for match in matches:
                        count, cell_type = match
                        # Converter a contagem para um número
                        count = int(count)

                        # Aqui, você pode adicionar a lógica para salvar os
                        if cell_type == 'RBC':
                            total_rbc += count
                        elif cell_type == 'WBC':
                            total_wbc += count
                        elif cell_type == 'Platelets':
                            total_plaquetas += count

                    print(f"Total RBC: {total_rbc}, Total WBC: {total_wbc}, Total Platelets: {total_plaquetas}")  # noqa: E501

                # move a imagem detectada do lab_results para outro lugar

                detected_objects = os.listdir('lab_results/')
                print(f"Detected objects: {detected_objects}")

                if detected_objects:  # Verifica se a lista não está vazia
                    latest_detection = detected_objects[-1]
                    source_path = os.path.join(
                        'lab_results', latest_detection)
                    destination_path = os.path.join(
                        'media/lab/detects', latest_detection)
                    shutil.move(source_path, destination_path)

                    # obtem a pk do imagem enviada
                    lab = Lab.objects.get(pk=lab.pk)
                    # salva os dados obtidos no bd da DetectedImage
                    detection_result = DetectedImage(
                        lab=lab,
                        detected_img=f'lab/detects/{latest_detection}',
                        total_wbc=total_wbc,
                        total_rbc=total_rbc,
                        total_plaquetas=total_plaquetas)
                    detection_result.save()

                    messages.success(
                        request, 'Sua imagem foi salva com sucesso!')
                else:
                    messages.error(
                        request, 'Nenhuma detecção encontrada em lab_results/.')  # noqa E501

                # Limpeza: remova o arquivo de saída, se desejar

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
                   'selected_patient': selected_patient,
                   'detected_objects': detected_objects})

# pesquisar paciente por nome e cpf


@has_permission_decorator('pesquisar_paciente')
def pesquisa(request):
    search_term = request.GET.get('q', '').strip()

    all_patients = Patient.objects.all()
    patients = []

    if search_term:
        patients = Patient.objects.filter(  # trocar customuser
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
        'all_patients': all_patients,
    })


# detalhes do usuario com opcoes de alterar dado e visu laudo
@login_required
@has_permission_decorator('pesquisar_paciente')
def usuario_detalhes(request, usuario_id):
    profile_user = get_object_or_404(
        Patient, pk=usuario_id)  # trocar customuser

    return render(request, 'lab/pages/usuario_detalhes.html',
                  {'profile_user': profile_user})


# alterar dados de um perfil selecionado
@login_required
@has_permission_decorator('alterar_dados')
def alterar_dados(request, usuario_id):
    profile_user = get_object_or_404(
        Patient, pk=usuario_id)  # trocar customuser

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile_user)
        if form.is_valid():
            form.save()

            return redirect('lab:usuario_detalhes', usuario_id=usuario_id)
    else:
        form = EditProfileForm(instance=profile_user)

    return render(request, 'lab/pages/alterar_dados.html', {
        'profile_user': profile_user, 'form': form})


# consultar laudos de um perfil
@has_permission_decorator('visualizar_laudo')
def laudo_perfil(request, usuario_id):
    profile_user = get_object_or_404(Patient,
                                     pk=usuario_id)
    laudos = Lab.objects.filter(patient=profile_user)

    return render(request, 'lab/pages/laudo_perfil.html',
                  {'profile_user': profile_user,
                   'laudos': laudos})


@has_permission_decorator('visualizar_laudo')
def laudo_detalhes(request, laudo_id):
    try:
        laudo = Lab.objects.get(id=laudo_id)
        detected_images = DetectedImage.objects.filter(lab=laudo)
    except Lab.DoesNotExist:
        raise Http404("O laudo não foi encontrado.")

    return render(request, 'lab/pages/laudo_detalhes.html', {
        'laudo': laudo,
        'detected_images': detected_images,
    })


# pesquisar laudos criados
@has_permission_decorator('visualizar_laudo')
def laudo_consultar(request):
    search_term = request.GET.get('q', '').strip()
    search_date = request.GET.get('search_date')

    all_reports = Lab.objects.all()
    reports = []

    if search_term:
        reports = Lab.objects.filter(
            Q(name__icontains=search_term) |
            Q(cpf__icontains=search_term)
        ).order_by('-id')

    if search_date:
        reports = Lab.objects.filter(
            created_at__date=search_date
        ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request, reports, PER_PAGE)

    return render(request, 'lab/pages/laudo_consultar.html', {
        'page_title': f'Pesquisar por "{search_term}" |',
        'search_term': search_term,
        'search_date': search_date,
        'all_reports': all_reports,
        'reports': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}&search_date={search_date}',
    })
