from django.urls import path
from . import views

urlpatterns =[
	path('Ajax-Load-Postu/', views.load_postu, name='ajax-load-postu'),
	path('Ajax-Load-Suku/', views.load_suku, name='ajax-load-suku'),
	path('Ajax-Load-Aldeia/', views.load_aldeia, name='ajax-load-aldeia'),
	path('Ajax-Load-Departamento/', views.load_dep, name='ajax-load-dep'),



]