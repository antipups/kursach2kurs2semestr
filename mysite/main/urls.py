from django.shortcuts import render
from django.urls import path
from django.views.generic import TemplateView
from .models import *
from . import views, querys, auth

urlpatterns = [
    path('',
         lambda request: render(request, 'content.html', views.dict_of_data), name='1'),
    path('mode/', views.hw, name='2'),
    path('work_with_tables/', views.mode, name='3'),
    path('task1/', views.task1_cont, name='4'),
    path('task2/', views.task2_cont, name='5'),
    path('task3/', views.task3_cont, name='6'),
    path('auth/',
         lambda request: render(request, 'auth.html', {}), name='8'),
    path('login/', auth.login_menu, name='9'),
    path('запросы/', querys.start, name='9'),
]
