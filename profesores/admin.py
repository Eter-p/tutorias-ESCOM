from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import Profesor

admin.site.site_title = "TUTORÍAS - Administración"
admin.site.site_header = "Panel de Administración"
admin.site.index_title = "Bienvenido al Administrador"

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'nombre','correo_alterno')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre', 'email', 'correo_alterno', 'username', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    list_display = ('username','nombre', 'email', 'correo_alterno', 'is_active', 'is_staff')
    search_fields = ('username', 'email')

admin.site.register(Profesor, CustomUserAdmin)
admin.site.unregister(Group)