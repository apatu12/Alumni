from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from alumni.models import Alumni, AlumniAddress

# dir. munisipiu
class APINotifBadgeDist(APIView):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		obj1 = Alumni.objects.filter(is_active=False).all().count()
		objects = obj1
		return Response({'value':objects})
