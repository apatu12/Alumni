from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from custom.models import Faculdade, Departamento, Municipality, \
     AdministrativePost, Village, SubVillage, Nasaun, Year, nivelmaster
from alumni.models import Alumni, AlumniAddress, AcademicRecord, \
    Career, FurtherStudy, AlumniUser


class APISexo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        facs = Faculdade.objects.all()

        labels = []
        mane = []
        feto = []

        for f in facs:
            m = AcademicRecord.objects.filter(
                alumni__sex="Masculino",
                faculty=f
            ).count()

            fe = AcademicRecord.objects.filter(
                alumni__sex="Femenino",
                faculty=f
            ).count()

            labels.append(f.code)  
            mane.append(m)         
            feto.append(fe)        
        data = {
            "label": labels,
            "obj_mane": mane,
            "obj_feto": feto,
        }
        return Response(data)
