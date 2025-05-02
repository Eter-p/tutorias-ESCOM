from django.contrib import admin
from django.contrib.auth.models import User,Group
from .models import Profesor
from .forms import FormProfesor

admin.site.site_title = "TUTORÍAS - Administración"
admin.site.site_header = "Panel de Administración"
admin.site.index_title = "Bienvenido al Administrador"

class ProfesorAdmin(admin.ModelAdmin):
    form = FormProfesor
    list_display = ('fecha',"nombre",'correo','correo_institucional')
    search_fields = ('nombre',)

admin.site.register(Profesor,ProfesorAdmin)
#admin.site.unregister(User)
admin.site.unregister(Group)