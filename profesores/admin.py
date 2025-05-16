from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import Profesor

admin.site.site_title = "TUTORÍAS - Administración"
admin.site.site_header = "Panel de Administración"
admin.site.index_title = "Bienvenido al Administrador"

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'correo_alterno', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'email', 'correo_alterno', 'is_staff')
    search_fields = ('username', 'email')

admin.site.register(Profesor, CustomUserAdmin)
# class ProfesorAdmin(admin.ModelAdmin):
#     form = FormProfesor
#     list_display = ("id","nombre",'correo_institucional','correo_alterno')
#     search_fields = ('nombre',)

admin.site.unregister(Group)