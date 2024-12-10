from django.db import models
from django.contrib.auth.models import User

class Registro(models.Model):
    name = models.CharField(max_length=50)  # Nombre único para cada máquina o fuente
    type_comp = models.CharField(max_length=10)
    active_power = models.FloatField()
    reactive_power = models.FloatField()
    factor = models.FloatField()
    S_power = models.FloatField()
    description = models.CharField(max_length=250, blank=True, null=True)
    hora = models.DateTimeField(null=True)
    hora_revision = models.DateTimeField(null=True)
    def __str__(self):
        return f"{self.name} ({self.type})"

class Revision(models.Model):
    name=models.CharField(max_length=45)
    observation= models.CharField(max_length=250)
    hora= models.DateTimeField(null=True)
    hecho = models.BooleanField(default=False)
    hora_hecho =models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.name} (Hecho: {'Sí' if self.hecho else 'No'})"
    
