from django.urls import path
from rango import views

app_name = 'rango'  # 命名空间

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]