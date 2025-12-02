from django.shortcuts import render
from alumni.models import Alumni
from custom.models import Municipality, Informativo, CarouselSlide, Faculdade
from django.db.models import Count, Q

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



def perfil(request):
    context={
        'title': 'Estatuto Da UNTL',
        'legend': 'Estatuto Da UNTL',
    }
    return render(request, 'Page/perfil.html', context)