from django.contrib import admin

from .models import DetectedImage, Lab


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ['name', 'cpf', 'created_at']  # Campos exibidos na lista
    list_filter = ['created_at']  # Filtros disponíveis
    search_fields = ['name', 'cpf']  # Pesquisa por nome e CPF
    list_per_page = 10


@admin.register(DetectedImage)
class DetectedAdmin(admin.ModelAdmin):
    list_display = ['lab', 'detected_img', 'total_wbc', 'total_rbc',
                    'total_plaquetas', 'total_deteccoes',
                    'concentracao_rbc', 'concentracao_wbc',
                    'concentracao_plaquetas', 'concentracao_wbc_rbc',
                    'media_diam_rbc', 'media_diam_wbc',
                    'media_circun_rbc', 'media_circun_rbc']
    list_per_page = 10
