from django.urls import path
from website import views

urlpatterns = [
	path('', views.webhome, name="web-home"),

]