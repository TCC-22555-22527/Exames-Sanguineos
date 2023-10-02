from django.contrib import admin

from .models import CustomUser, Tec


class TecAdmin(admin.ModelAdmin):
    # Adicione 'crm' ao list_display
    list_display = ('user', 'crm')


admin.site.register(Tec, TecAdmin)
admin.site.register(CustomUser)
# Registra TecProfile com classe personalizada, se necessário
