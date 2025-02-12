from django.urls import path
from rango import views
from django.contrib import admin
from django.urls import include


app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]