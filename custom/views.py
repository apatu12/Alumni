from django.shortcuts import render, redirect
from custom.models import Municipality, AdministrativePost, Village, SubVillage, Departamento
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def load_postu(request):
    municipality_id = request.GET.get('mun')
    post = AdministrativePost.objects.filter(municipality_id=municipality_id).order_by('name')
    return render(request, 'ajax/load_postu.html', {'post': post})

def load_suku(request):
    administrativepost_id = request.GET.get('post')
    suku = Village.objects.filter(administrativePost_id=administrativepost_id).order_by('name')
    return render(request, 'ajax/load_suku.html', {'suku': suku})

def load_aldeia(request):
    suku_id = request.GET.get('suk')
    aldeia = SubVillage.objects.filter(village_id=suku_id).order_by('name')
    return render(request, 'ajax/load_aldeia.html', {'aldeia': aldeia})

def load_dep(request):
    faculty_id = request.GET.get('faculty')
    dep = Departamento.objects.filter(faculdade_id=faculty_id).order_by('name')
    return render(request, 'ajax/load_dep.html', {'dep': dep})

