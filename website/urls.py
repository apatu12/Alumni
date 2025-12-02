from django.urls import path
from website import views

urlpatterns = [
	path('', views.webhome, name="web-home"),
	path('register/', views.reg_info, name='reg-info'),
	path('add/', views.antigosalunos_create, name='alunos_add'),
    path('address/<str:hashed>/', views.aluno_address, name='aluno_address'),
    path('estudo/<str:hashed>/', views.aluno_estudo, name='aluno_estudo'),
    path('cont-carrer/<str:hashed>/', views.aluno_carrer, name='aluno_carrer'),
    path('cont-estudo/<str:hashed>/', views.aluno_further, name='est-est'),
    path("ajax/pos-form/", views.ajax_pos_form, name="ajax-pos-form"),
	path('verify/<str:hashed>/', views.alumni_verify, name='alumni_verify'),


	path('Perfil-Page.html/', views.perfil, name='al-perf'),

]