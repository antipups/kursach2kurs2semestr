from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def hw(request):
    print('Hello World')
    if request.method == 'POST':
        print(request.POST)
    elif request.method == 'GET':
        print('GET')
    return HttpResponse('Hello World')
