from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class Recpt(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True,
        related_name='recpt_profile')
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username


class Tec(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True,
        related_name='tec_profile')
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    crm = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True,
        related_name='patient_profile')
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    birthday = models.DateField()
    street = models.CharField(max_length=65)
    number = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14)
    cell = models.CharField(max_length=15, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    fk_recpt = models.ForeignKey(Recpt, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}"
