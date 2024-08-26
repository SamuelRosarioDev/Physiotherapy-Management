from django.urls import path
from django.contrib import admin
from app_physiotherapy import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    
    path('created', views.create_users, name='create_users'),
    path('list', views.login_users, name='login_users'),
    path('admin', admin.site.urls),
]
