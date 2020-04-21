from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import views
import util


@csrf_exempt
def start(request):
    # print(request.POST)
    dict_of_data = dict(request.POST)
    request.session['dict_of_data'].update({'dict_of_all': dict(util.sum_all_methods_for_querys(dict_of_data))})
    return render(request, "querys.html", {'dict_of_all': dict(util.sum_all_methods_for_querys(dict_of_data))})
