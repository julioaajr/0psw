# Generated by Django 4.2.6 on 2023-10-05 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exames', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipoexames',
            name='horario_final',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='tipoexames',
            name='horario_inicial',
            field=models.IntegerField(null=True),
        ),
    ]
