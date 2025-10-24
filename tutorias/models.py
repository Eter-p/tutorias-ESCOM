from django.db import models
from django.utils.timezone import now
from profesores.models import Profesor

class Periodo(models.Model):
    nombre_periodo = models.CharField(unique=True,max_length=100,null=True,blank=True,default="202_-_")
    fecha_apertura = models.DateTimeField(null=True,blank=True,default=now)
    fecha_cierre = models.DateTimeField(null=True,blank=True,default=now)
    
    def __str__(self):
        return f"{self.nombre_periodo}"
    
    class Meta:
        verbose_name = "Periodo"
        verbose_name_plural = "Periodos"

class Tutorias(models.Model):
    periodo = models.ForeignKey(Periodo,on_delete=models.CASCADE,blank=True,null=True)
    profesor = models.ForeignKey(Profesor,on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15)
    fecha = models.DateTimeField(null=True,blank=True,default=now)
    
    def __str__(self):
        return f"{self.profesor.username} - {self.id }"
    
    class Meta:
        verbose_name = "Tutoría"
        verbose_name_plural = "Tutorías"
    
class TutoriaGrupal(models.Model):
    tutoria = models.ForeignKey(Tutorias,on_delete=models.CASCADE,default=None)
    grupo = models.CharField(max_length=6)
    unidad_aprendizaje = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    no_hombres_grupal = models.SmallIntegerField()
    no_mujeres_grupal = models.SmallIntegerField()
    lista_alumnos_grupal = models.CharField(max_length=100)
    tutoria_asignada = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.tutoria}"
    class Meta:
        verbose_name = "Tutoría grupal"
        verbose_name_plural = "Tutorías Grupales"

class TutoriaPares(models.Model):
    tutoria = models.ForeignKey(Tutorias,on_delete=models.CASCADE,default=None)
    nombre_pares = models.CharField(max_length=100)
    boleta_pares = models.CharField(max_length=12)
    unidad_pares = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f"{self.tutoria}"
    class Meta:
        verbose_name = "Tutoría entre Pares"
        verbose_name_plural = "Tutorías entre Pares"
        
class TutoriaIndividual(models.Model):
    tutoria = models.ForeignKey(Tutorias,on_delete=models.CASCADE,default=None)
    no_hombres_individual = models.SmallIntegerField()
    no_mujeres_individual = models.SmallIntegerField()
    lista_alumnos_individual = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tutoria}"
    class Meta:
        verbose_name = "Tutoría individual"
        verbose_name_plural = "Tutorías individuales"

class TutoriaMovilidad(models.Model):
    tutoria = models.ForeignKey(Tutorias,on_delete=models.CASCADE,default=None)
    boleta_nombre = models.CharField(max_length=100)
    no_hombres_movilidad = models.SmallIntegerField()
    no_mujeres_movilidad = models.SmallIntegerField()

    def __str__(self):
        return f"{self.tutoria}"
    class Meta:
        verbose_name = "Tutoría de Movilidad"
        verbose_name_plural = "Tutorías de Movilidad"

class TutoriaRegularizacion(models.Model):
    tutoria = models.ForeignKey(Tutorias,on_delete=models.CASCADE,default=None)
    unidad_aprendizaje_regularizacion = models.CharField(max_length=100)
    carrera_regularizacion = models.CharField(max_length=100)
    no_hombres_regularizacion = models.SmallIntegerField()
    no_mujeres_regularizacion = models.SmallIntegerField()
    lista_alumnos_regularizacion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tutoria}"
    class Meta:
        verbose_name = "Tutoría de Regularización"
        verbose_name_plural = "Tutorías de Regularización"

class TutoriaRecuperacion(models.Model):
    tutoria = models.ForeignKey(Tutorias,on_delete=models.CASCADE,default=None)
    unidad_aprendizaje_recuperacion = models.CharField(max_length=100,verbose_name="Unidad de aprendizaje")
    carrera_recuperacion = models.CharField(max_length=100,verbose_name="Carrera")
    no_hombres_recuperacion = models.SmallIntegerField()
    no_mujeres_recuperacion = models.SmallIntegerField()
    lista_alumnos_recuperacion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tutoria}"
    class Meta:
        verbose_name = "Tutoría de Recuperación"
        verbose_name_plural = "Tutorías de Recuperación"
        
class ReporteExcel(models.Model):
    periodo = models.ForeignKey(Periodo,on_delete=models.CASCADE,blank=True,null=True)
    carrera = models.CharField(max_length=100,verbose_name="Carrera")
    hombres_regular = models.IntegerField(default=0,verbose_name="Hombres regulares")
    mujeres_regular = models.IntegerField(default=0,verbose_name="Mujeres regulares")
    hombres_irregular = models.IntegerField(default=0,verbose_name="Hombres irregulares")
    mujeres_irregular = models.IntegerField(default=0,verbose_name="Mujeres irregulares")
    def __str__(self):
        return f"{self.periodo} - {self.carrera}"
    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"