# Generated by Django 4.2.4 on 2023-11-10 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0005_detectedimage_lab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detectedimage',
            name='detected_img',
            field=models.ImageField(blank=True, default='', upload_to='lab/detects/'),
        ),
    ]
