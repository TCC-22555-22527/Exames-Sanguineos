from django.contrib import admin

from .models import CustomUser, Patient, Recpt, Tec

admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Tec)
admin.site.register(Recpt)

# Registra TecProfile com classe personalizada, se necessário
