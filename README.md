# Diagnose

## Português (pt-br)

## Sistema de Gerenciamento de Laboratório de Sangue

### Visão Geral
Este é um sistema web desenvolvido em Django projetado para um laboratório de sangue.

### Funcionalidades

#### Tipos de Usuários:
- Técnico: Os técnicos são responsáveis por enviar imagens microscópicas de sangue para a geração de relatórios usando o processamento YOLO AI, resultando em relatórios de hemograma.
- Recepcionista: Os recepcionistas gerenciam os registros de pacientes e controlam seus dados pessoais, com a capacidade de fazer modificações.
- Paciente: Os pacientes têm acesso aos seus relatórios de hemograma usando seu CPF.
  
### Processamento de Imagens:
Utiliza YOLO AI, OpenCV, Darknet para processar imagens microscópicas de sangue e gerar relatórios de hemograma.

#### Gerenciamento de Usuários:
Permite que os recepcionistas gerenciem registros de pacientes e controlem seus dados pessoais.
Acesso do Paciente:

Os pacientes podem acessar seus relatórios de hemograma usando seu CPF.

## English (en-us)

### Overview: 
This is a Django-based web system for a blood laboratory. 

### Features

User Types: The system supports three types of users: technician, receptionist, and patient.

Image Processing: Utilizes YOLO AI for processing microscopic blood images to generate hemogram reports.

User Management: Allows receptionists to manage patient registrations and control their personal data.
Patient Access: Patients can access their hemogram reports using their CPF.
