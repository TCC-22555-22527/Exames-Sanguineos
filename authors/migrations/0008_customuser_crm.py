# Generated by Django 4.2.4 on 2024-02-15 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0007_remove_customuser_is_patient_user_tec_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='crm',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]