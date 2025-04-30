from django.db import models
from django.utils.timezone import now

class Profesor(models.Model):
    fecha = models.DateTimeField(null=True,blank=True,default=now)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100,default=None,blank=True)
    correo_institucional = models.EmailField(max_length=100,default=None,unique=True)

    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"