# Generated by Django 4.2.4 on 2023-11-12 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0007_detectedimage_average_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detectedimage',
            name='average_size',
        ),
    ]
