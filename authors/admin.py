from django.contrib import admin

from .models import CustomUser, Patient, Tec

admin.site.register(CustomUser)
admin.site.register(Patient)
admin.site.register(Tec)

# Registra TecProfile com classe personalizada, se necessário
