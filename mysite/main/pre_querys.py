from .models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import views


@csrf_exempt
def zapolnenie(request):
    dict_of_data = request.session['dict_of_data']
    dict_of_data.update({
        'first_querys': tuple(str(row.getter()[0]) + ' | ' + row.getter()[1] for row in Type.objects.all()),
        'second_querys': tuple(str(row.getter()[0]) + ' | ' + row.getter()[2] for row in Pharmacy.objects.all()),
        'fifth_querys': tuple(str(row.getter()[0]) + ' | ' + row.getter()[1] for row in Manufacturer.objects.all()),
        'sixth_querys_district': tuple(str(row.getter()[0]) + ' | ' + row.getter()[1] for row in District.objects.all()),
        'sixth_querys_medicament': tuple(str(row.getter()[0]) + ' | ' + row.getter()[1] for row in Medicament.objects.all()),
        'eigth_querys': tuple(str(row.getter()[0]) + ' | ' + row.getter()[3] + ' ' + row.getter()[2][0] + '. ' + row.getter()[4][0] + '.' for row in Employee.objects.all()),
        'tenth_querys': tuple(str(row.getter()[0]) + ' | ' + row.getter()[1] for row in Shape.objects.all()),
        'tenth_querys_name_of_medicament': tuple(str(row.getter()[0]) + ' | ' + row.getter()[1] for row in Name_of_medicament.objects.all()),

    })
    return render(request, 'pre_querys.html', dict_of_data)
