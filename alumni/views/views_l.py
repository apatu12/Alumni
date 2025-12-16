import csv, io, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count, Prefetch
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
from django.views.decorators.csrf import csrf_exempt


