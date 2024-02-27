from django.contrib.auth.models import AbstractUser
from django.db import models
from project import settings


class CustomUser(AbstractUser):

    birthday = models.DateField(null=True, blank=True)
    street = models.CharField(max_length=65, blank=True)
    number = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    cpf = models.CharField(max_length=16, blank=True)
    crm = models.CharField(max_length=16, blank=True)
    user_type = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.username


class UserType(models.Model):
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.type


class Recpt(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default="tec")
    last_name = models.CharField(max_length=30, default="tec")
    fk_user_type = models.ForeignKey(
        UserType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return self.user.username


class Tec(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default="tec")
    last_name = models.CharField(max_length=30, default="tec")
    crm = models.CharField(max_length=16)
    fk_user_type = models.ForeignKey(UserType,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True)

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE),
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField()
    street = models.CharField(max_length=65)
    number = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    cpf = models.CharField(max_length=16)
    recpt_fk = models.ForeignKey(Recpt,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True)
    fk_user_type = models.ForeignKey(UserType,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True)

    def __str__(self):
        return f"Paciente: {self.first_name} {self.last_name}"
