import csv, io, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count, Prefetch
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from alumni.forms import *
from django.contrib import messages
from config.decorators import allowed_users
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
import pandas as pd
from tablib import Dataset
from django.utils.text import slugify
import dateparser
from django.shortcuts import render, redirect
import pandas as pd
from custom.models import Faculdade, Departamento, Municipality, \
     AdministrativePost, Village, SubVillage, Nasaun, Year, nivelmaster
from alumni.models import Alumni, AlumniAddress, AcademicRecord, \
    Career, FurtherStudy, AlumniUser
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
@allowed_users(allowed_roles=['Admin', 'Vice_Reitor', 'Staff'])
def home_Alumni(request):
    group = request.user.groups.all()[0].name
    objects1, objects2 = [],[]
    fac = Faculdade.objects.all()
    totm = 0
    totf = 0
    totmf = 0

    for data in fac:
        data1 = AcademicRecord.active_objects.filter(alumni__sex="Masculino", faculty=data).count()
        data2 = AcademicRecord.active_objects.filter(alumni__sex="Femenino", faculty=data).count()
        totalfac = data1 + data2
        objects1.append([data, data1, data2, totalfac])
        totm += data1
        totf += data2
        totmf += totalfac

    context = {
        'page':'Home',
        'title': 'Sumario Geral Antigos ALunos',
        'legend': 'Sumario Geral Antigos ALunos',
        'objects1':objects1,'totm':totm, 'totf':totf, 'totmf':totmf
    }
    return render(request, 'Alumni/List.html', context)

@login_required
@allowed_users(allowed_roles=['Admin','Vice_Reitor','Staff'])
def Alumnilist(request):
    group = request.user.groups.all()[0].name
    anos = Year.objects.all()  
    objects = (
        Alumni.active_objects.filter(is_active=True).select_related('academic__faculty', 'address__mun') 
        .order_by('-id'))
    context = {
        'page': 'Alumni',
        'objects': objects,
        'title': 'Lista Dos Antigos Alunos',
        'legend': 'Lista Dos Antigos Alunos',
        'group': group,
        'ano': anos,
    }
    return render(request, 'Alumni/List.html', context)


@login_required
@allowed_users(allowed_roles=['Admin','Staff'])
def new_submit(request):
    group = request.user.groups.all()[0].name
    objects = Alumni.active_objects.filter(is_active=False).order_by('-id')
    context = {
        'page': 'Alumni_active',
        'objects': objects,
        'title': 'Lista Dos Antigos Alunos  Nova Submição',
        'legend': 'Lista Dos Antigos Alunos Nova Submição',
        'group': group,
    }
    return render(request, 'Alumni/List_submit.html', context)


@login_required
@allowed_users(allowed_roles=['Admin','Vice_Reitor','Staff'])
def Alumnilist_print(request):
    group = request.user.groups.all()[0].name
    anos = Year.objects.all()  
    objects = Alumni.active_objects.filter(is_active=True).order_by('-id')
    context = {
        'page': 'Alumi',
        'objects': objects,
        'title': 'Lista Dos Antigos Alunos',
        'legend': 'Lista Dos Antigos Alunos',
        'group': group,
        'ano': anos,
    }
    return render(request, 'Alumni/List_print.html', context)



@csrf_exempt
@login_required
@allowed_users(allowed_roles=['Admin'])
def alumni_ajax_update(request):
    if request.method == "POST":
        ids = request.POST.getlist("ids[]")
        action = request.POST.get("action")
        if action == "activate":
            Alumni.objects.filter(id__in=ids).update(is_active=True)
            message = "Antigos Alunos foram ativados com sucesso!"
        elif action == "deactivate":
            Alumni.objects.filter(id__in=ids).update(is_active=False)
            message = "Antigos Alunos desativados com sucesso!"
        else:
            return JsonResponse({"error": "Invalid action"}, status=400)
        return JsonResponse({
            "updated_ids": ids,
            "message": message
        })
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
@allowed_users(allowed_roles=['Admin','Vice_Reitor','Staff'])
def alumni_detail(request, hashed):
    alumni = (
        Alumni.objects
        .select_related(
            "address",
            "academic",
            "created_by",
            "updated_by"
        )
        .prefetch_related(
            Prefetch("careers"),
            Prefetch("further_studies")
        )
        .filter(is_active=True)
    )
    alumni = get_object_or_404(alumni, hashed=hashed)
    context = {
        "alumni": alumni,
        "address": getattr(alumni, "address", None),
        "academic": getattr(alumni, "academic", None),
        "careers": alumni.careers.all(),
        "studies": alumni.further_studies.all(),
        'title': f'Detailho Dados Do Antigo Aluno {alumni.name}',
        'legend': f'Detailho Dados Do Antigo Aluno {alumni.name}',
    }

    return render(request, "Alumni/Detaillu.html", context)