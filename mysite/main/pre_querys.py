from .models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import views


@csrf_exempt
def zapolnenie(request):
    print()
    views.dict_of_data.update({
        'first_querys': tuple(str(row.getter()[0]) + ' | ' + row.getter()[1] for row in Type.objects.all()),
    })
    return render(request, 'pre_querys.html', views.dict_of_data)
