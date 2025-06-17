"""
URL configuration for proyTutorias project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from profesores import views as vprof
from tutorias import views as vtuto

urlpatterns = [
    path('',vprof.inicio,name="inicio"),
    path('admin/', admin.site.urls),
    path('administrador/',vprof.inicio_administrador,name="administrador"),
    path('administrador/tutorias/<str:tipo>/<str:periodo>/',vtuto.listar_tutorias_admin,name="listar_tutorias_admin"),
    path('administrador/tutorias/grupales/<str:periodo>/reporte',vprof.reporte,name="reporte"),
    path('tutorias/<str:tipo>/',vtuto.listar_tutorias_user,name="listar_tutorias_user"),
    path('administrador/profesores/<str:periodo>/',vprof.listar_profesores,name="profesores"),
    path('registro/tutoria/<str:tipo>/',vtuto.registrar_tutoria,name="registrar_tutoria"),
    path('login/',vprof.signin,name="login"),
    path('logout/',vprof.signout,name="logout"),
    path('signup/',vprof.signup,name="signup"),
    path('test/',vprof.test,name="test"),
]
