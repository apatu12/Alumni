"""
URL configuration for si_alumni project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import handler404, handler500
from main import views as main_views

admin.site.site_title ='SI-ALUMNI-UNTL'
admin.site.site_header ='SI-ALUMNI-UNTL'
admin.site.index_title ='SI-ALUMNI-UNTL'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls'), name='web-home'),
    path('Admin-Home.html/', main_views.home, name='index'),
    path('Login-Page.html/', main_views.loginPage, name='login'),
    path('logout-Page.html/', main_views.logout_view, name='logout'),
]
handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'
