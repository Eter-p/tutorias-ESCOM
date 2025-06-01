from django.db import models
from django.contrib.auth.models import AbstractUser

class Profesor(AbstractUser):
    first_name = None
    last_name = None
    
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, unique=True, verbose_name="Correo institucional")
    correo_alterno = models.EmailField(max_length=100, default=None, blank=True, null=True)
    
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"] 
    
    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
