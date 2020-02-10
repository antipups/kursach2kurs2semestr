from django.urls import path
from django.views.generic import ListView, DetailView
from .models import Person
# from django.contrib import admin

from . import views

urlpatterns = [
    path('',
         ListView.as_view(queryset=Person.objects.all(),
                          # template_name='templates\\index.html'
                          template_name='C:\\Users\\kurku\\PycharmProjects\\kursach2kurs2semestr\\mysite\\main\\templates\\index.html'),
         name='hw'),
    # path('admin/', admin.site.urls),
]
