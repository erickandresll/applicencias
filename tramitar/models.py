from django.db import models

class nomina_funcionario(models.Model):
    run = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    centro_de_costo = models.CharField(max_length=100)
    tipo_contrato = models.CharField(max_length=100)

class renta_funcionario(models.Model):
    run = models.CharField(max_length=10)
    mes = models.IntegerField()
    año = models.IntegerField()
    tipo_salud = models.CharField(max_length=100)
    imponible = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('run', 'mes', 'año')

class nomina_licencia(models.Model):
    folio = models.CharField(primary_key=True, max_length=20)
    run = models.CharField(max_length=12)
    fecha_emision = models.DateField()
    fecha_inicio = models.DateField()
    dias = models.IntegerField()
    tipo_licencia = models.CharField(max_length=100)
    tipo_repo = models.CharField(max_length=100)
    run_profesional = models.CharField(max_length=10)
    nombre_profesional = models.CharField(max_length=100)
    apellido_profesional = models.CharField(max_length=100)
    tipo_profesional = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    cotizante = models.CharField(max_length=100)
