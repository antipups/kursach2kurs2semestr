from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import views
import util


@csrf_exempt
def start(request):
    views.dict_of_data.update(util.sum_all_methods_for_querys())
    return render(request, "querys.html", views.dict_of_data)
