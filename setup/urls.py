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
    path('delete_schedule/<int:id>/', views.delete_schedule, name='delete_schedule'), 
    path('payment_page/', views.payment_page, name='payment_page'),
    path('mark_as_paid/<int:id>/', views.mark_as_paid, name='mark_as_paid'),
    
    path('list_sessions/', views.list_sessions, name='list_sessions'),
    path('progress_session/', views.progress_session, name='progress_session'),
    
    path('admin/', admin.site.urls),
]
