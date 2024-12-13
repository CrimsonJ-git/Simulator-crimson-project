# Generated by Django 5.1.3 on 2024-12-04 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type_comp', models.CharField(max_length=10)),
                ('active_power', models.FloatField()),
                ('reactive_power', models.FloatField()),
                ('factor', models.FloatField()),
                ('S_power', models.FloatField()),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('hora', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('observation', models.CharField(max_length=250)),
                ('hora', models.DateTimeField(auto_now_add=True)),
                ('hecho', models.BooleanField(default=False)),
            ],
        ),
    ]
