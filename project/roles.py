from rolepermissions.roles import AbstractUserRole


class TecUser (AbstractUserRole):
    available_permissions = {'laudo_enviar_permission': True,
                             'visualizar_laudo': True,
                             'pesquisar_paciente': True,
                             'pagina_inicial': True
                             }


class RecptUSer (AbstractUserRole):
    available_permissions = {'cadastrar_paciente': True,
                             'visualizar_laudo': True,
                             'alterar_dados': True,
                             'pagina_inicial': True,
                             'pesquisar_paciente': True
                             }


class PatientUser (AbstractUserRole):
    available_permissions = {'visualizar_laudo': True,
                             'pagina_inicial': True
                             }
