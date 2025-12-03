from django.urls import path
from alumni import views

urlpatterns =[
	path('Lista-Alumni.html/', views.Alumnilist, name='a-list'),
	path('Lista-Alumni-print.html/', views.Alumnilist_print, name="ap-list"),
	path("alumni/detail/<str:hashed>/", views.alumni_detail, name="al-detail"),
	path('Nova-Submicao.html/', views.new_submit, name='a-submit'),
	path('alumni/ajax-update/', views.alumni_ajax_update, name="alumni_ajax_update"),
	path('alumni/home/', views.home_Alumni, name='al-home'),

]