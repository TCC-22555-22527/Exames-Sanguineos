from autoslug import AutoSlugField
from django.db import models


class Lab(models.Model):
    name = models.CharField(max_length=65)
    cpf = models.CharField(max_length=19)
    slug = AutoSlugField(unique=True, populate_from='name')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='lab/reports/', blank=True, default='')
