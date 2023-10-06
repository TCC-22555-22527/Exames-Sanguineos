
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
