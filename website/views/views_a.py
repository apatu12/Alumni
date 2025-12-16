from django.shortcuts import render
from alumni.models import Alumni, AcademicRecord, Faculdade, Year
from custom.models import Municipality, Informativo, CarouselSlide, Faculdade
from django.db.models import Count, Q, Prefetch
from django.utils.crypto import md5



# Create your views here.
def webhome(request):
    total = Alumni.objects.count()
    slides = CarouselSlide.objects.filter(is_active=True).order_by('order')
    informativos = Informativo.objects.filter(is_active=True).order_by('-created_at')[:4]
    totm = Alumni.objects.filter(sex='Masculino').count()
    totf = Alumni.objects.filter(sex='Feto').count()
    mun = Municipality.objects.annotate(
        male_count=Count('alumniaddress__alumni', filter=Q(alumniaddress__alumni__sex='Masculino')),
        female_count=Count('alumniaddress__alumni', filter=Q(alumniaddress__alumni__sex='Femenino'))
    )
    objects1 = [
        [m, m.male_count, m.female_count, m.male_count + m.female_count]
        for m in mun
    ]
    fac = Faculdade.objects.annotate(
        male_count=Count('academicrecord__alumni', filter=Q(academicrecord__alumni__sex='Masculino')),
        female_count=Count('academicrecord__alumni', filter=Q(academicrecord__alumni__sex='Femenino'))
    )
    objects2 = [
        [f, f.male_count, f.female_count, f.male_count + f.female_count]
        for f in fac
    ]
    context = {
        'legend': 'Pajina lista Alumni',
        'total': total,
        'objects1': objects1,
        'objects2': objects2,
        'totm': totm,
        'totf': totf,
        'slides': slides,
        'informativos': informativos,
        'title': "Universidade Nacional Timor Lorosa'e (UNTL)",
    }
    return render(request, 'website/home.html', context)

def alumni_dashboard_ultra(request):
    # Filters
    faculty_id = request.GET.get("faculty")
    year_id = request.GET.get("year")

    # Base query
    alumni = (
        Alumni.active_objects
        .select_related("academic__faculty", "academic__year_graduation")
        .prefetch_related("careers")
        .all()
    )

    if faculty_id:
        alumni = alumni.filter(academic__faculty_id=faculty_id)

    if year_id:
        alumni = alumni.filter(academic__year_graduation_id=year_id)

    context = {
        "alumni": alumni.order_by("-created_at")[:50],  # tampilkan 50 saja agar ringan
        "faculties": Faculdade.objects.all().order_by("name"),
        "years": Year.objects.all().order_by("name"),

        # Stats
        "total": alumni.count(),
        "male": alumni.filter(sex="Masculino").count(),
        "female": alumni.filter(sex="Femenino").count(),
    }

    return render(request, 'Page/alumni.html', context)

def perfil(request):
    context={
        'title': 'Estatuto Da UNTL',
        'legend': 'Estatuto Da UNTL',
    }
    return render(request, 'Page/perfil.html', context)