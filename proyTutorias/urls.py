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
from formulario import views as vf
from tutorias import views as vt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',vf.formulario,name="inicio"),
    path('administrador/',vf.administrador,name="administrador"),
    path('administrador/tutoria/<str:tipo>',vt.lista_tutorias,name="lista_tutorias"),
    path('formulario/',vf.formulario,name="formulario"),
    path('signin/',vf.signin,name="signin"),
    path('logout/',vf.signout,name="logout"),
]
