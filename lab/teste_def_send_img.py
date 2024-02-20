@has_permission_decorator('laudo_enviar_permission')
def send_img(request):
    form = AuthorReportForm()
    selected_patient = None
    detected_objects = None

    total_rbc = 0
    total_wbc = 0
    total_platelets = 0

    # conversao para micrometros 'um'
    resolution_pixels_per_um = 25400
    sizes_of_bounding_boxes_um = []

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

                # Obtem o caminho da imagem que foi enviada e salva
                image_path = os.path.join('media/' + lab.image.name)
                # comando para detectar objetos na imagem
                detect_command = (
                    "python yolov5/Inference_files/detect.py "
                    f"--source {image_path} "
                    "--weights yolov5/Inference_files/best_BCCM.pt "
                    "--output lab_results/ --save-txt"
                )

                # Execute o comando e redirecione a saída para o arquivo
                subprocess.run(detect_command, shell=True)

                txt_filename = os.path.splitext(
                    os.path.basename(image_path))[0] + ".txt"
                txt_filepath = os.path.join('lab_results', txt_filename)

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

                    messages.success(
                        request, 'Sua imagem foi salva com sucesso!')
                else:
                    messages.error(
                        request, 'Nenhuma detecção encontrada em lab_results/.')  # noqa E501

            except Patient.DoesNotExist:
                messages.error(request, 'Paciente não encontrado.')
        else:
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

    return render(request, 'lab/pages/send_img.html',
                  {'patients': patients,
                   'form': form,
                   'selected_patient': selected_patient,
                   'detected_objects': detected_objects})
