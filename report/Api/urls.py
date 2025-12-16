from django.urls import path
from . import views_re

urlpatterns = [
    path('fun/sexo/', views_re.APISexo.as_view()),
]