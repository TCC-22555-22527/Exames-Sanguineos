from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_patient_user = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)
    street = models.CharField(max_length=65, blank=True)
    number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    cpf = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.username


class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField()
    street = models.CharField(max_length=65)
    number = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    cpf = models.CharField(max_length=16)

    def __str__(self):
        return self.user.username  # Ou outra representação que você preferir


class Tec(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    crm = models.IntegerField()


class Recpt(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
