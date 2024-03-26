import os
import re
import shutil
import subprocess
from math import pi

from authors.forms import AuthorReportForm, EditProfileForm
from authors.models import Patient, Recpt, Tec
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from rolepermissions.decorators import has_permission_decorator
from utils.pagination import make_pagination

from .models import BackupImage, DetectedImage, Lab

PER_PAGE = os.environ.get('PER_PAGE', 9)


# funcao específica do superusuário
@login_required(login_url='authors:login', redirect_field_name='next')
def register_custom_user(request):
    return render(request, 'lab/pages/register_custom_user.html')


# funções de usuários comuns
@login_required(login_url='authors:login', redirect_field_name='next')
def home(request):
    if request.user.is_superuser:
        adm_instance = request.user.is_superuser
        return render(request, 'lab/pages/home.html', {
            'adm': adm_instance
        })
    else:
        try:
            recpt_instance = request.user.recpt_profile
            return render(request, 'lab/pages/home.html', {
                'recpt': recpt_instance,
            })
        except Recpt.DoesNotExist:
            pass

        try:
            tec_instance = request.user.tec_profile
            return render(request, 'lab/pages/home.html', {
                'tec': tec_instance,
            })
        except Tec.DoesNotExist:
            pass

        try:
            patient_instance = request.user.patient_profile
            return render(request, 'lab/pages/home.html', {
                'patient': patient_instance,
            })
        except Patient.DoesNotExist:
            pass


@login_required(login_url='authors:login', redirect_field_name='next')
def about(request):
    return render(request, 'lab/pages/about.html')


# envio de imagem estando logado como técnico ou administrador
@login_required(login_url='authors:login', redirect_field_name='next')
@has_permission_decorator('laudo_enviar_permission')
def send_img(request):
    form = AuthorReportForm(
        data=request.POST or None,
        files=request.FILES or None,
    )
    selected_patient = None
    detected_objects = None
    processing_state = None
    total_rbc = 0
    total_wbc = 0
    total_platelets = 0

    # conversao para micrometros 'um'
    resolution_pixels_per_um = 25400
    sizes_of_bounding_boxes_um = []

    if request.method == 'POST':
        processing_state = 'processing'
        # captura a imagem enviada no form
        image = request.FILES.get('image')
        # captura o paciente selecionado
        selected_patient_id = request.POST.get('selected_patient')
        print(f'selected_pat:{selected_patient_id}')

        # caso os valores sejam verdadeiros
        if selected_patient_id and image:
            try:
                # obtem o id do paciente selecionado
                selected_patient = Patient.objects.get(
                    user_id=selected_patient_id)
                # salva a imagem e os dados do paciente no bd
                backup_img = BackupImage(
                    image=image
                )
                backup_img.save()
                # Defina o caminho do arquivo de saída que vai ter rbc, etc.

                # Obtem o caminho da imagem que foi enviada e salva
                image_path = os.path.join('media/' + backup_img.image.name)
                print(f"Caminho da imagem: {image_path}")
                # comando para detectar objetos na imagem
                detect_command = (
                    "python yolo/Inference_files/detect.py "
                    f"--source {image_path} "
                    "--weights yolo/Inference_files/best_BCCM.pt "
                    "--output lab_results/ --save-txt"
                )

                # Execute o comando e redirecione a saída para o arquivo
                subprocess.run(detect_command, shell=True)

                txt_filename = os.path.splitext(
                    os.path.basename(image_path))[0] + ".txt"
                txt_filepath = os.path.join('lab_results', txt_filename)

                # verifica se a imagem enviada não segue os padrões
                if not os.path.exists(txt_filepath):
                    messages.error(
                        request, ('Essa imagem não segue os padrões '
                                  'do sistema. Envie uma imagem de sangue '
                                  'microscópica.')
                    )
                    return redirect('lab:send_img')

                with open(txt_filepath, "r") as txt_file:
                    txt_content = txt_file.readlines()

                # Imprima o conteúdo do arquivo de texto para análise
                print("Conteúdo do arquivo de texto:")
                print("".join(txt_content))

                # Leia a saída do arquivo após o término do processo

                # Agora, você pode processar 'output_content' para extrair
                matches = re.findall(
                    r'(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)', "".join(txt_content))  # noqa E501
                print(f"Matches: {matches}")

                if matches:
                    # Iterar sobre as correspondências
                    for match in matches:
                        class_id, x_center, y_center, width, height = match
                        # Converter a contagem para um número
                        print(f"Class ID: {class_id}")

                        x_center = float(x_center)
                        y_center = float(y_center)
                        width = float(width)
                        height = float(height)

                        # Converta para micrômetros usando a resolução
                        x_center_um = x_center * resolution_pixels_per_um
                        y_center_um = y_center * resolution_pixels_per_um
                        width_um = width * resolution_pixels_per_um
                        height_um = height * resolution_pixels_per_um

                        # área das bounding boxes
                        area_um2 = width_um * height_um
                        # salva na lista todas as áreas
                        sizes_of_bounding_boxes_um.append(area_um2)
                        average_size = sum(sizes_of_bounding_boxes_um) / len(
                            sizes_of_bounding_boxes_um) if sizes_of_bounding_boxes_um else 0  # noqa E501

                        if class_id == '0':
                            total_platelets += 1
                        elif class_id == '1':
                            total_rbc += 1
                        elif class_id == '2':
                            total_wbc += 1

                        total_detects = total_rbc + total_wbc + total_platelets  # noqa E501

                        concentration_rbc = round(
                            (total_rbc / total_detects) * 100, 2)
                        concentration_wbc = round(
                            (total_wbc / total_detects) * 100, 2)
                        concentration_platelets = round(
                            (total_platelets / total_detects) * 100, 2)
                        concentration_wbc_rbc = round(total_wbc / total_rbc, 4) if total_rbc != 0 else 0  # noqa E501
                        media_diam_rbc = round(sum([float(match[3]) + float(match[4]) for match in matches if match[0] == '1']) / total_rbc * resolution_pixels_per_um, 2) if total_rbc != 0 else 0  # noqa E501
                        media_diam_wbc = round(sum([float(match[3]) + float(match[4]) for match in matches if match[0] == '2']) / total_wbc * resolution_pixels_per_um, 2) if total_wbc != 0 else 0  # noqa E501
                        media_circun_rbc = round(sum([(float(match[3]) + float(match[4])) / 4 * 2 * pi for match in matches if match[0] == '1']) / total_rbc * resolution_pixels_per_um, 2) if total_rbc != 0 else 0  # noqa E501
                        media_circun_wbc = round(sum([(float(match[3]) + float(match[4])) / 4 * 2 * pi for match in matches if match[0] == '2']) / total_wbc * resolution_pixels_per_um, 2) if total_wbc != 0 else 0  # noqa E501

                        # dividindo por mil para obter o valor em micrometros
                        media_diam_rbc = round(media_diam_rbc / 1000, 2)
                        media_diam_wbc = round(media_diam_wbc / 1000, 2)
                        media_circun_rbc = round(media_circun_rbc / 1000, 2)
                        media_circun_wbc = round(media_circun_wbc / 1000, 2)

                # impressoes no terminal
                print(
                    f"\nTotal de objetos detectados: {total_detects}")  # noqa E501
                print(
                f"\nTotal RBC: {total_rbc}, Total WBC: {total_wbc}, Total Platelets: {total_platelets}")  # noqa E501
                print(
                    f"Coordenadas normalizadas (x, y, largura, altura): {x_center}, {y_center}, {width}, {height}")  # noqa E501
                print(
                    f"Coordenadas em micrometros (x, y, largura, altura): {x_center_um}, {y_center_um}, {width_um}, {height_um}")   # noqa E501
                print(
                    f"Área da bounding box em micrometros quadrados: {area_um2}, Tamanho médio em micrometros quadrados: {average_size}")  # noqa E501
                print(
                    f"\nConcentracao de RBC detectados: {concentration_rbc} %")  # noqa E501
                print(
                    f"\nConcentracao de WBC detectados: {concentration_wbc} %")  # noqa E501
                print(
                    f"\nConcentracao de Plaquetas detectadas: {concentration_platelets} %")  # noqa E501
                print(
                    f"\nConcentracao de WBC por RBC: {concentration_wbc_rbc}")  # noqa E501
                print(
                    f"\nDiametro medio RBC: {media_diam_rbc} um")
                print(
                    f"\nDiametro medio WBC {media_diam_wbc} um")
                print(
                    f"\nCircunferencia media RBC {media_circun_rbc} um")  # noqa E501
                print(
                    f"\nCircunferencia media WBC {media_circun_wbc} um")  # noqa E501

                detected_objects = os.listdir('lab_results/')
                print(f"\nDetected objects: {detected_objects}")

                if request.user.is_superuser:
                    lab = Lab(patient=selected_patient,
                              fk_tec=None,
                              name=selected_patient.first_name,
                              cpf=selected_patient.cpf,
                              image=image)
                    lab.save()
                else:
                    fk_tec = Tec.objects.get(user=request.user)
                    print(f"fk_tec: {fk_tec}")

                    lab = Lab(patient=selected_patient,
                              fk_tec=fk_tec,
                              name=selected_patient.first_name,
                              cpf=selected_patient.cpf,
                              image=image)
                    lab.save()

                if detected_objects:  # Verifica se a lista não está vazia
                    latest_detection = next((f for f in detected_objects if f.lower().endswith(('.png', '.jpg', '.jpeg'))), None)  # noqa E501

                    source_path = os.path.join(
                        'lab_results', latest_detection)
                    destination_path = os.path.join(
                        'media/lab/detects', latest_detection)
                    shutil.move(source_path, destination_path)
                    print(f"\nultima detecção: {latest_detection}")
                    # obtem a pk do imagem enviada
                    lab = Lab.objects.get(pk=lab.pk)
                    # salva os dados obtidos no bd da DetectedImage
                    detection_result = DetectedImage(
                        lab=lab,
                        detected_img=f'lab/detects/{latest_detection}',
                        total_wbc=total_wbc,
                        total_rbc=total_rbc,
                        total_platelets=total_platelets,
                        total_detects=total_detects,
                        concentration_rbc=concentration_rbc,
                        concentration_wbc=concentration_wbc,
                        concentration_platelets=concentration_platelets,
                        concentration_wbc_rbc=concentration_wbc_rbc,
                        media_diam_rbc=media_diam_rbc,
                        media_diam_wbc=media_diam_wbc,
                        media_circun_rbc=media_circun_rbc,
                        media_circun_wbc=media_circun_wbc)
                    detection_result.save()

                    processing_state = 'success'
                    messages.success(
                        request, 'Sua imagem foi salva com sucesso e o laudo '
                        'foi gerado. Veja abaixo!')
                    return redirect('lab:report_detail', report_id=lab.pk)

                else:
                    processing_state = 'error'
                    messages.error(
                        request, 'Nenhuma detecção encontrada em lab_results/.')  # noqa E501

            except Patient.DoesNotExist:
                processing_state = 'error'
                messages.error(request, 'Paciente não encontrado.')
        else:
            processing_state = 'error'
            messages.error(
                request, 'Preencha todos os campos antes de enviar.')

        return redirect('lab:send_img')

    patients = Patient.objects.all()

    if request.method == 'GET' and 'q' in request.GET:
        search_term = request.GET['q'].strip()
        patients = Patient.objects.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(cpf__icontains=search_term)
        )

    # paginação
    page_obj, pagination_range = make_pagination(
        request, patients, 5)

    has_search_results = bool(patients)

    return render(request, 'lab/pages/send_img.html',
                  {'patients': page_obj,
                   'has_search_results': has_search_results,
                   'pagination_range': pagination_range,
                   'form': form,
                   'selected_patient': selected_patient,
                   'detected_objects': detected_objects,
                   'processing_state': processing_state,
                   }
                  )


# pesquisar paciente por nome e cpf
@login_required(login_url='authors:login', redirect_field_name='next')
@has_permission_decorator('pesquisar_paciente')
def search_patient(request):
    search_term = request.GET.get('q', '').strip()

    all_patients = Patient.objects.all().order_by('-user_id')
    patients = []

    if search_term:
        patients = Patient.objects.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term) |
            Q(cpf__icontains=search_term)
        ).order_by('-user_id')

    page_obj, pagination_range = make_pagination(
        request, patients, 6)

    page_obj_all, pagination_range_all = make_pagination(
        request, all_patients, 6)

    has_search_results = bool(patients)

    return render(request, 'lab/pages/search_patient.html', {
        'page_title': f'Pesquisar por "{search_term}" |',
        'search_term': search_term,
        'patients': page_obj,
        'all_patients': page_obj_all,
        'pagination_range': pagination_range,
        'pagination_range_all': pagination_range_all,
        'additional_url_query': f'&q={search_term}',
        'has_search_results': has_search_results,
    })


# detalhes do usuario com opcoes de alterar dado e visu laudo
@login_required(login_url='authors:login', redirect_field_name='next')
@has_permission_decorator('pesquisar_paciente')
def patient_detail(request, user_id):
    profile_user = get_object_or_404(
        Patient, pk=user_id)

    return render(request, 'lab/pages/patient_detail.html',
                  {'profile_user': profile_user})


# alterar dados de um perfil selecionado
@login_required(login_url='authors:login', redirect_field_name='next')
@has_permission_decorator('alterar_dados')
def edit_patient_data(request, user_id):
    profile_user = get_object_or_404(
        Patient, pk=user_id)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile_user)
        if form.is_valid():
            form.save()

            return redirect('lab:patient_detail', user_id=user_id)
    else:
        form = EditProfileForm(instance=profile_user)

    return render(request, 'lab/pages/edit_patient_data.html', {
        'profile_user': profile_user, 'form': form})


# consultar laudos de um perfil
@login_required(login_url='authors:login', redirect_field_name='next')
@has_permission_decorator('visualizar_laudo')
def reports_profile(request, user_id):
    profile_user = get_object_or_404(Patient,
                                     pk=user_id)
    reports = Lab.objects.filter(patient=profile_user).order_by('-id')

    return render(request, 'lab/pages/reports_profile.html',
                  {'profile_user': profile_user,
                   'reports': reports})


# Detalhes de um determinado laudo c/ image pré e pós detecção
@login_required(login_url='authors:login', redirect_field_name='next')
@has_permission_decorator('visualizar_laudo_detalhe')
def report_detail(request, report_id):
    try:
        report = Lab.objects.get(id=report_id)

        # Verifica se o usuário é do tipo "paciente"
        if hasattr(request.user, 'patient_profile'):
            # Verifica se o laudo pertence ao paciente atual
            if report.patient != request.user.patient_profile:
                raise Http404("Você não tem permissão para acessar essa URL.")
            else:
                detected_images = DetectedImage.objects.filter(lab=report)
                return render(request, 'lab/pages/report_detail.html', {
                    'report': report,
                    'detected_images': detected_images,
                })
        else:
            detected_images = DetectedImage.objects.filter(lab=report)

    except Lab.DoesNotExist:
        raise Http404("O laudo não foi encontrado.")

    return render(request, 'lab/pages/report_detail.html', {
        'report': report,
        'detected_images': detected_images,
    })


# pesquisar laudos criados
@login_required(login_url='authors:login', redirect_field_name='next')
@has_permission_decorator('visualizar_laudo')
def report_search(request):
    search_term = request.GET.get('q', '').strip()
    search_date = request.GET.get('search_date')

    all_reports = Lab.objects.all().order_by('-id')
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
        request, reports, 12)

    page_obj_all, pagination_range_all = make_pagination(
        request, all_reports, 12)

    has_search_results = bool(reports)
    # Inicializa a query apenas com search_term
    additional_url_query = f'&q={search_term}'

    if search_date:  # Adiciona search_date à query apenas se estiver presente
        additional_url_query += f'&search_date={search_date}'

    return render(request, 'lab/pages/report_search.html', {
        'page_title': f'Pesquisar por "{search_term}" |',
        'search_term': search_term,
        'search_date': search_date,
        'all_reports': page_obj_all,
        'reports': page_obj,
        'pagination_range': pagination_range,
        'pagination_range_all': pagination_range_all,
        'additional_url_query': additional_url_query,
        'has_search_results': has_search_results,
    })
