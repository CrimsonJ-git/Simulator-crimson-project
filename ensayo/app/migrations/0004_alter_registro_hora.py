# Generated by Django 5.1.3 on 2024-12-05 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_registro_hora_revision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro',
            name='hora',
            field=models.DateTimeField(),
        ),
    ]
