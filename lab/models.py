from authors.models import Patient
from django.db import models


class Lab(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=65)
    cpf = models.CharField(max_length=19)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='lab/reports/', blank=True, default='')

    def __str__(self):
        return f"Laboratório de {self.patient.first_name} ({self.cpf})"


class DetectedImage(models.Model):
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    detected_img = models.ImageField(
        upload_to='lab/detects/', blank=True, default='')
    total_wbc = models.IntegerField(default=0)
    total_rbc = models.IntegerField(default=0)
    total_plaquetas = models.IntegerField(default=0)
    total_deteccoes = models.IntegerField(default=0)
    concentracao_rbc = models.FloatField(default=0.0)
    concentracao_wbc = models.FloatField(default=0.0)
    concentracao_plaquetas = models.FloatField(default=0.0)
    concentracao_wbc_rbc = models.FloatField(default=0.0)
    media_diam_rbc = models.FloatField(default=0.0)
    media_diam_wbc = models.FloatField(default=0.0)
    media_circun_rbc = models.FloatField(default=0.0)
    media_circun_wbc = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.lab} - {self.detected_img}"
