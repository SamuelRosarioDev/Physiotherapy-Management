from django.urls import path
from django.contrib import admin
from app_physiotherapy import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    
    path('create/', views.create_users, name='create_users'),
    path('portal/', views.login_users, name='login_users'),
    path('portal/scheduling/', views.create_schedule, name='create_schedule'),
    
    path('admin', admin.site.urls),
]