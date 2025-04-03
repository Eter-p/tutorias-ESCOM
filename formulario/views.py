from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404

def hello(request):
	return HttpResponse(f'HOLA MUNDO')

def index(request):
    return render(request,"index.html",{
		'NOTA': "HOLA MUNDO",
	})

def formulario(request):
    return render(request,"formulario.html",{
		'NOTA': "HOLA MUNDO",
	})
