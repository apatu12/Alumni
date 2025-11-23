from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group
from user.models import AuditLogin
import json
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import os
from urllib.parse import urlparse
from django.urls import resolve
from config.decorators import allowed_users
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    group = request.user.groups.all()[0].name
    context = {
        'group': group,
    }
    return render(request, 'home/home.html', context)

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            ip = get_client_ip(request)
            AuditLogin.objects.create(
                user=user,
                ip_address=ip,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                status='SUCCESS'
            )
            return redirect('index')
        else:
            ip = get_client_ip(request)
            AuditLogin.objects.create(
                user=None,
                ip_address=ip,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                status='FAILED'
            )
            messages.error(request, 'Username ou Password la loos! Favor Prense fali!')

    context = {
        "title": "Pajina Login",
    }
    return render(request, 'auth/login.html', context)


def error_404(request, exception):
        data = {}
        return render(request,'auth/404.html', data)

def error_500(request):
        data = {}
        return render(request,'auth/500.html', data)

