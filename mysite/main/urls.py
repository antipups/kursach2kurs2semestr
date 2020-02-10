from django.urls import path
from django.views.generic import ListView, DetailView
from .models import *


urlpatterns = [
    path('',
         ListView.as_view(queryset=Product.objects.all(),   # всё работает , только тут доделай, и в index html
                          template_name='index.html'),
         name='hw'),
]
