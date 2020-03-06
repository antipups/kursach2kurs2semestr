from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import views


@csrf_exempt
def login_menu(request):
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user is not None:
        views.dict_of_data.update({'user': True,
                                   'username': user.get_full_name()})
        return render(request, 'content.html', views.dict_of_data)
    else:
        return render(request, 'content.html', views.dict_of_data)
