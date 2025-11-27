from django.db import models

# Create your models here.

class Aprendiz(models.Model):
    documento_identidad = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()
    correo_electronico = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    ciudad = models.CharField(max_length=100)
    programa = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.documento_identidad}"