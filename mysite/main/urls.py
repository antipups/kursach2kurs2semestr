from django.shortcuts import render
from django.urls import path
from django.views.generic import ListView, DetailView
from .models import *
from . import views


urlpatterns = [
    path('',
         lambda request: render(request, 'content.html', views.dict_of_data), name='sex'),
    path('mode/', views.hw, name='sex2'),
]
