# Diagnose
Site - https://www.diagnose.helielsouza.com.br/
Linkedin post - 
 
## Português (pt-br)

## Sistema de Gerenciamento de Laboratório de Sangue

### Visão Geral
Esta é uma aplicação web desenvolvida em Django projetada para um laboratório de sangue, com o objetivo de acelerar informações preliminares de um exame de sangue e ter uma asseguridade maior no controle e gerenciamento de todos os tipos de funcionários

![image](https://github.com/TCC-22555-22527/Exames-Sanguineos/assets/127799256/41b8c2ce-d847-4a20-8716-3aa59cfcc327)
![image](https://github.com/TCC-22555-22527/Exames-Sanguineos/assets/127799256/1c5d7750-23da-48f8-909b-ae3ce7bc709f)


#### Funcionalidades
- Pagína "Meu Perfil" para visualizar todas as suas operações e dados pessoais;
- Página inicial onde você pode obter instruções de uso;
- Página exclusiva para administradores e usuários do tipo técnico, que possibilita o envio de imagens sanguíneas microscópicas de acordo com o usuário que teve o sangue coletado, que em seguida serão processadas através de um modelo de rede neural que ira gerar um laudo hematológico com dados premiliares para uma avaliação mais precisa;
- Localizar pacientes cadastrados no sistema, para visualizar seus dados pessoais, alterá-los se for o caso (exclusivos para administradores e recepcionistas) e também visualizar todos os laudos cadastrados em seu respectivo CPF;
- Apenas o usuário do tipo paciente não tem acesso, há uma página que possui um campo de busca que permite você filtrar laudos já enviados de acordo com o cpf de determinado paciente, além de uma lista dos laudos cadastrados mais recentemente;
- Página que conta melhor sobre como o sistema foi criado e por quem, além de explicar melhor o objetivo e tecnologias utilizadas;
- Página que permite o acesso ao formulário de cadastro de pacientes no sistema, exclusiva para administradores e recepcionistas;
- Página de cadastro de todos os tipos de funcionários (somente usuários administradores tem acesso à essa página);

                    
##### Principais funcões dos 4 tipos de usuários:
- Técnico: Os técnicos são responsáveis por enviar imagens microscópicas de sangue para a geração de relatórios usando o processamento YOLO AI, resultando em relatórios de hemograma, além de poder consultar todos os laudos já existentes no sistema, no perfil de algum paciente, ou laudos que ele já enviou.
- Recepcionista: Os recepcionistas gerenciam os registros de pacientes e controlam seus dados pessoais, com a capacidade de fazer modificações, visualizar perfis desses pacientes e ter acesso a todos os usuários pacientes que ele já cadastrou.
- Paciente: Os pacientes têm acesso aos seus relatórios de hemograma criados em seu CPF.
- Administradores: Tem poder total no sistema, como cadastro de técnicos, recepcionistas e pacientes, assim como controlar e visualizar todas as informações do sistema.

  
#### Processamento de Imagens:
O laudo hematológico (ou hemograma) é gerado quando o usuário técnico realiza o upload de uma imagem sanguínea microscópica, onde uma rede neural convolucional (CNN), que foi treinada através de um algoritmo de detecção de objetos chamado YOLO e também um dataset de mais de 400 imagens sanguíneas microscópicas, irá detectar, contar e calcular todos os parâmetros a partir das células sanguíneas detectadas (leucócitos, hemácias e plaquetas), gerando o laudo. O algoritmo YOLO foi treinado com o framework Darknet, no Google Colab. Foram utilizadas bibliotecas como o OpenCV e Pillow neste treinamento.  
![image](https://github.com/TCC-22555-22527/Exames-Sanguineos/assets/127799256/ad701301-e406-4199-8416-1bee7848a4be)
![image](https://github.com/TCC-22555-22527/Exames-Sanguineos/assets/127799256/25f9e602-f15e-4c05-bbe5-9ebf71c7c90b)


#### Tecnologias de desenvolvimento utilizadas:
- Django: Framework web fullstack, que trabalha na arquitetura MTV;
- HTML/CSS: Estruturação e estilizacação das páginas, onde ela está totalmente responsiva em todas os dispotivos;
- Django Templates: Para reaproveitamento de componentes HTML;
- Jquery, AJAX e JavaScript: Com o objetivo de melhorar a interatividade do usuário no navegador;


#### Tecnologias usadas na implatação (Deploy):
- VPS ubuntu 23.04 64 bit: Servidor utilizado para hospedagem, acessada por chave SSH;
- Nginx: Servidor web utilizado para configuração de uploads e de roteamento das requisições HTTP para o diretório dentro do servidor;
- Gunicorn: um servidor HTTP WSGI (Web Server Gateway Interface), como camada intermediária da aplicação Django com o Nginx;
- PostgreSQL: Banco de dados utilizado;
- GIT: Versionamento de código;
- Repositório Bare: repositório remoto e transitório que atuou no meio de campo entre o desenvolvimento local e a aplicação em produção para o versionamento de código;
- Socket.unix: comunicação interprocessual (IPC) entre processos em sistemas Unix-like;
- Certificado SSL para proteção;

## English (en-us)

## Blood Laboratory Management System

### Overview
This is a web application developed in Django designed for a blood laboratory, aiming to accelerate preliminary blood test information and provide greater assurance in the control and management of all types of employees.

![image](https://github.com/TCC-22555-22527/Exames-Sanguineos/assets/127799256/41b8c2ce-d847-4a20-8716-3aa59cfcc327)
![image](https://github.com/TCC-22555-22527/Exames-Sanguineos/assets/127799256/1c5d7750-23da-48f8-909b-ae3ce7bc709f)

#### Features
- "My Profile" page to view all your operations and personal data;
- Homepage where you can get usage instructions;
- Exclusive page for administrators and technician-type users, which allows the submission of microscopic blood images according to the user who had the blood collected, which will then be processed through a neural network model that will generate a hematological report with preliminary data for a more accurate evaluation;
- Find registered patients in the system, to view their personal data, modify them if necessary (exclusive to administrators and receptionists), and also view all reports registered under their respective CPF;
- Only the patient-type user does not have access, there is one page has a search field that allows you to filter already submitted reports according to the CPF of a particular patient, as well as a list of the most recently registered reports;
- Page that explains more about how the system was created and by whom, in addition to better explaining the objective and technologies used;
- Page that allows access to the patient registration form in the system, exclusive to administrators and receptionists;
- Page for registering all types of employees (only administrators have access to this page);


#### Main functions of the 4 user types:
- Technician: Technicians are responsible for submitting microscopic blood images for report generation using YOLO AI processing, resulting in hematogram reports, as well as being able to consult all existing reports in the system, in a patient's profile, or reports they have already submitted.
- Receptionist: Receptionists manage patient records and control their personal data, with the ability to make modifications, view profiles of these patients, and have access to all patient users they have already registered.
- Patient: Patients have access to their hematogram reports created under their CPF.
- Administrators: Have full power in the system, such as registering technicians, receptionists, and patients, as well as controlling and viewing all system information.


#### Image Processing:
The hematological report (or hematogram) is generated when the technician user uploads a microscopic blood image, where a Convolutional Neural Network (CNN), which was trained through an object detection algorithm called YOLO and also a dataset of over 400 microscopic blood images, will detect, count, and calculate all parameters from the detected blood cells (leukocytes, erythrocytes, and platelets), generating the report. The YOLO algorithm was trained with the Darknet framework, on Google Colab. Libraries such as OpenCV and Pillow were used in this training.
![image](https://github.com/TCC-22555-22527/Exames-Sanguineos/assets/127799256/ad701301-e406-4199-8416-1bee7848a4be)
![image](https://github.com/TCC-22555-22527/Exames-Sanguineos/assets/127799256/25f9e602-f15e-4c05-bbe5-9ebf71c7c90b)

#### Development Technologies Used:
- Django: Full-stack web framework, working on the MTV architecture;
- HTML/CSS: Structuring and styling of pages, where it is fully responsive on all devices;
- Django Templates: For HTML component reuse;
- Jquery, AJAX, and JavaScript: Aimed at improving user interactivity in the browser;


#### Deployment Technologies Used:
- VPS ubuntu 23.04 64 bit: Server used for hosting accessed by SSH key;
- Nginx: Web server used for upload configuration and routing HTTP requests to the directory within the server;
- Gunicorn: a WSGI (Web Server Gateway Interface) HTTP server, as an intermediate layer of the Django application with Nginx;
- PostgreSQL: Database used;
- GIT: Code versioning;
- Bare Repository: remote and transitory repository that acted in the midfield between local development and application in production for code versioning;
- Socket.unix: interprocess communication (IPC) between processes in Unix-like systems;
- SSL certificate for protection;





