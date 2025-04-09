from django.contrib import admin

from .models import Tutorias,TutoriaGrupal,TutoriaPares,TutoriaIndividual,TutoriaMovilidad,TutoriaRegularizacion
from .forms import FormTutorias,FormTutoriaGrupal,FormTutoriaPares,FormTutoriaIndividual,FormTutoriaMovilidad,FormTutoriaRegularizacion

class TutoriasAdmin(admin.ModelAdmin):
    form = FormTutorias
    list_display = ("id","tipo","profesor")
    search_fields = ('profesor__profesor',)
    list_filter = ('tipo',)

class TutoriaGrupalAdmin(admin.ModelAdmin):
    form = FormTutoriaGrupal
    list_display = ("tutoria","grupo","unidad_aprendizaje","carrera","no_hombres_grupal","no_mujeres_grupal","lista_alumnos_grupal")
    search_fields = ("tutoria__profesor__profesor","grupo","unidad_aprendizaje")
    list_filter = ("carrera",)

class TutoriaParesAdmin(admin.ModelAdmin):
    form = FormTutoriaPares
    list_display = ("tutoria","nombre_pares","boleta_pares")
    search_fields = ("tutoria__profesor__profesor",)

class TutoriaIndividuaAdmin(admin.ModelAdmin):
    form = FormTutoriaIndividual
    list_display = ("tutoria","no_hombres_individual",'no_mujeres_individual','lista_alumnos_individual')
    search_fields = ("tutoria__profesor__profesor",)

class TutoriaMovilidadAdmin(admin.ModelAdmin):
    form = FormTutoriaMovilidad
    list_display = ("tutoria","boleta_nombre","no_hombres_movilidad","no_mujeres_movilidad")
    search_fields = ("tutoria__profesor__profesor",)

class TutoriaRegularizacionAdmin(admin.ModelAdmin):
    form = FormTutoriaRegularizacion
    list_display = ("tutoria","unidad_aprendizaje_regularizacion","carrera_regularizacion","no_hombres_regularizacion","no_mujeres_regularizacion","lista_alumnos_regularizacion")
    search_fields = ("tutoria__profesor__profesor","unidad_aprendizaje_regularizacion")
    list_filter = ("carrera_regularizacion",)


admin.site.register(Tutorias,TutoriasAdmin)
admin.site.register(TutoriaGrupal,TutoriaGrupalAdmin)
admin.site.register(TutoriaPares,TutoriaParesAdmin)
admin.site.register(TutoriaIndividual,TutoriaIndividuaAdmin)
admin.site.register(TutoriaMovilidad,TutoriaMovilidadAdmin)
admin.site.register(TutoriaRegularizacion,TutoriaRegularizacionAdmin)