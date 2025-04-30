from django import forms
from .models import Profesor

class FormProfesor(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = [
            "nombre",
            "correo",
            "correo_institucional"
        ]
        labels = {
            "nombre" : "Nombre",
            "correo" : "Correo electronico",
            "correo_institucional" : "Correo instucional"
        }