from django.db import models

class Profesor(models.Model):
    profesor = models.CharField(max_length=100)
    correo = models.CharField(max_length=100,default=None)
    correo_institucional = models.CharField(max_length=100,default=None)

    def __str__(self):
        return f"{self.profesor}"
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"

