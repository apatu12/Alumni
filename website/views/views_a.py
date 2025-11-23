from django.shortcuts import render

# Create your views here.
def webhome(request):
    context = {
        'title': "Universidade Nacional Timor Lorosa'e (UNTL)",
    }
    return render(request, 'website/layout.html', context)