# Generated by Django 5.0.1 on 2024-01-04 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='nomina_funcionario',
            fields=[
                ('run', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('cargo', models.CharField(max_length=100)),
                ('centro_de_costo', models.CharField(max_length=100)),
                ('tipo_contrato', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='nomina_licencia',
            fields=[
                ('folio', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_emision', models.DateField()),
                ('fecha_inicio', models.DateField()),
                ('dias', models.IntegerField()),
                ('tipo_licencia', models.CharField(max_length=100)),
                ('tipo_repo', models.CharField(max_length=100)),
                ('run_profesional', models.CharField(max_length=10)),
                ('nombre_profesional', models.CharField(max_length=100)),
                ('apellido_profesional', models.CharField(max_length=100)),
                ('tipo_profesional', models.CharField(max_length=100)),
                ('especialidad', models.CharField(max_length=100)),
                ('cotizante', models.CharField(max_length=100)),
                ('run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tramitar.nomina_funcionario')),
            ],
        ),
        migrations.CreateModel(
            name='renta_funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run', models.CharField(max_length=10)),
                ('mes', models.IntegerField()),
                ('año', models.IntegerField()),
                ('tipo_salud', models.CharField(max_length=100)),
                ('imponible', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'unique_together': {('run', 'mes', 'año')},
            },
        ),
    ]
