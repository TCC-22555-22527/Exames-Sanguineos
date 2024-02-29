from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass


class Recpt(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.user.username


class Tec(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    crm = models.CharField(max_length=16)

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    birthday = models.DateField()
    street = models.CharField(max_length=65)
    number = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    cpf = models.CharField(max_length=16)
    fk_recpt = models.ForeignKey(Recpt, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.username}"
    # fk_user_type = models.ForeignKey(UserType,on_delete=models.SET_NULL,
    # null=True,blank=True)#noqa E501
