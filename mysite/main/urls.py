from django.shortcuts import render
from django.urls import path
from django.views.generic import ListView, DetailView
from .models import *
from . import views


urlpatterns = [
    path('',
         lambda request: render(request, 'content.html', views.dict_of_data), name='sex'),
    path('mode/', views.hw, name='sex2'),
    path('work_with_tables/', views.mode, name='sex3'),
    path('task1/', views.task1_cont, name='sex4'),
    path('task2/', views.task2_cont, name='sex5'),
    # path('task3/', views.task3_cont, name='sex6'),
]
