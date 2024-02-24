from django.contrib import admin

from .models import CustomUser, Patient, Recpt, Tec, UserType

admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Tec)
admin.site.register(Recpt)


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    ordering = ['id']

    class Meta:
        verbose_name_plural = "Tipos de Usuário"


# Registra TecProfile com classe personalizada, se necessário
