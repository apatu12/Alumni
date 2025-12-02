import csv, io, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string 
from django.db.models import Q, Count
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
from alumni.forms import AlumniForm, AlumniAddressForm, AcademicRecordForm, CareerForm, FurtherStudyForm
from config.utils import generate_random_string, getjustnewid, hash_md5

def reg_info(request):
    context = {
        'title':'Registo Antigos Alunos',
        'legend':'Registo Antigos Alunos',
    }
    return render(request, 'alunos_reg/home.html', context)

def antigosalunos_create(request):
    if request.method == "POST":
        form = AlumniForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            newid = getjustnewid(Alumni)
            instance.hashed = hash_md5(newid)
            instance.save()
            messages.success(request, 'Dados Pessoais Registrado Com Suseso!')
            return redirect('aluno_address', hashed=instance.hashed)
    else:
        form = AlumniForm()
    context = {
        'form': form,
        'title': 'Registo Antigos Alunos',
        'legend': 'Registo Dados Pesoal Antigos Alunos'
    }
    return render(request, 'alunos_reg/form12.html', context)

def aluno_address(request, hashed):
    try:
        aluno = Alumni.active_objects.get(hashed=hashed)
    except Alumni.DoesNotExist:
        messages.error(request, "Dados la hetan!")
        return redirect('reg_info')

    # Cari alamat jika sudah ada, kalau belum buat instance baru
    address, created = AlumniAddress.objects.get_or_create(alumni=aluno)

    if request.method == "POST":
        form = AlumniAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Susesu")
            return redirect('aluno_estudo', hashed=aluno.hashed)
    else:
        form = AlumniAddressForm(instance=address)

    context = {
        'form': form,
        'title': 'Registo Naturalidade',
        'legend': 'Registo Naturalidade',
    }
    return render(request, 'alunos_reg/form12.html', context)



def aluno_estudo(request, hashed):
    try:
        aluno = Alumni.active_objects.get(hashed=hashed)
    except Alumni.DoesNotExist:
        messages.error(request, "Dados laiha!")
        return redirect('reg_info')

    if request.method == "POST":
        form = AcademicRecordForm(request.POST)
        if form.is_valid():
            study = form.save(commit=False)
            study.alumni = aluno
            study.save()
            messages.success(request, 'Estudo Registrado com Suseso!')
            return redirect('aluno_carrer', hashed=aluno.hashed)
    else:
        form = AcademicRecordForm()

    context = {
        'form': form,
        'title': 'Registo Estudo Académico',
        'legend': 'Registo Estudo Académico',
    }
    return render(request, 'alunos_reg/form12.html', context)


def aluno_status(request, hashed):
    aluno = Alumni.objects.get(hashed=hashed)
    if request.method == "POST":
        form = AlumniStatusForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect("alumni_verify", hashed=aluno.hashed)

    else:
        form = AlumniStatusForm(instance=aluno)
    context = {
        "form": form, 
        "aluno": aluno,
        'title': 'Registo Status Atual',
        'legend': 'Registo Status Atual'
    }
    return render(request, "alunos_reg/form12.html", context)



def aluno_carrer(request, hashed):
    try:
        aluno = Alumni.active_objects.get(hashed=hashed)
    except Alumni.DoesNotExist:
        messages.error(request, "Dados laiha!")
        return redirect('reg_info')

    if request.method == "POST":
        form = CareerForm(request.POST)
        if form.is_valid():
            study = form.save(commit=False)
            study.alumni = aluno
            study.save()
            messages.success(request, 'Estudo Registrado com Suseso!')
            return redirect('est-est', hashed=aluno.hashed)
    else:
        form = CareerForm()

    context = {
        'form': form,
        'title': 'Registo Estudo Académico',
        'legend': 'Registo Estudo Académico',
    }
    return render(request, 'alunos_reg/form12.html', context)

def aluno_further(request, hashed):
    try:
        aluno = Alumni.active_objects.get(hashed=hashed)
    except Alumni.DoesNotExist:
        messages.error(request, "Dados laiha!")
        return redirect('reg_info')
    if request.method == "POST":
        form = FurtherStudyForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.alumni = aluno
            fs.save()
            messages.success(request, "Dados  registrado com suseso!")
            messages.warning(request, "Favor Verifica antes De Submeter!")
            return redirect('alumni_verify', hashed=aluno.hashed)
    else:
        form = FurtherStudyForm()

    context = {
        'form': form,
        'title': 'Estudo Continua',
        'legend': 'Estudo Continua',
    }
    return render(request, 'alunos_reg/form12.html', context)

def alumni_verify(request, hashed):
    try:
        alumni = Alumni.active.get(hashed=hashed)
    except Alumni.DoesNotExist:
        messages.error(request, "Ddados la hetan!")
        return redirect('reg_info')
    address = AlumniAddress.objects.filter(alumni=alumni).first()
    academic = AcademicRecord.objects.filter(alumni=alumni).first()
    careers = Career.objects.filter(academic=academic)
    further_studies = FurtherStudy.objects.filter(alumni=alumni)
    if request.method == "POST":
        alumni.verified = True
        alumni.save()

        messages.success(request, "Dados ita hotu-hotu confirma ona!")
        return redirect('alumni_success')
    context = {
        'title': 'Verifika Dado',
        'legend': 'Verifica Todos Dados',
        'alumni': alumni,
        'address': address,
        'academic': academic,
        'careers': careers,
        'further': further_studies
    }
    return render(request, 'alunos_reg/verify.html', context)


def ajax_pos_form(request):
    pos = request.GET.get("pos")
    hashed = request.GET.get("hashed")

    study_form = None
    career_form = None
    outro = False

    if pos == "Em Estudo":
        study_form = FurtherStudyForm()

    elif pos == "No Trabalho":
        career_form = CareerForm()

    elif pos == "Em Estudo e No Trabalho":
        study_form = FurtherStudyForm()
        career_form = CareerForm()

    elif pos == "Outro":
        outro = True

    html = render_to_string("alunos_reg/partials/pos_dynamic_form.html", {
        "study_form": study_form,
        "career_form": career_form,
        "outro": outro
    })

    return HttpResponse(html)


def aluno_status(request, hashed):
    aluno = Alumni.objects.get(hashed=hashed)
    if request.method == "POST":
        form = AlumniStatusForm(request.POST, instance=aluno)
        if form.is_valid():
            obj = form.save()
            pos = obj.pos
            if pos == "Em Estudo" or pos == "Em Estudo e No Trabalho":
                study_form = FurtherStudyForm(request.POST)
                if study_form.is_valid():
                    study = study_form.save(commit=False)
                    study.alumni = aluno
                    study.save()

            if pos == "No Trabalho" or pos == "Em Estudo e No Trabalho":
                career_form = CareerForm(request.POST)
                if career_form.is_valid():
                    career = career_form.save(commit=False)
                    career.alumni = aluno
                    career.save()

            if pos == "Outro":
                aluno.pos_outro = request.POST.get("pos_outro")
                aluno.save()

            messages.success(request, "Status atualizado!")
            return redirect("next_step")

    else:
        form = AlumniStatusForm(instance=aluno)

    return render(request, "alunos_reg/form12.html", {"form": form})
