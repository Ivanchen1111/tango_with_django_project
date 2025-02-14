from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('set_cookie/', views.set_cookie, name='set_cookie'),
    path('get_cookie/', views.get_cookie, name='get_cookie'),
    path('update_cookie/', views.update_cookie, name='update_cookie'),
    path('delete_cookie/', views.delete_cookie, name='delete_cookie'),
    path('set_session/', views.set_session_view, name='set_session'),
    path('get_session/', views.get_session_view, name='get_session'),
    path('delete_session/', views.delete_session_view, name='delete_session'),
]
