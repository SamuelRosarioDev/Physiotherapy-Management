from django.urls import path
from django.contrib import admin
from app_physiotherapy import views

from django.urls import path


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('create/', views.UserCreateView.as_view(), name='create_users'),
    path('portal/', views.LoginView.as_view(), name='login_users'),
    path('portal/scheduling/', views.SchedulerCreateView.as_view(), name='create_schedule'),
    path('list_sessions/', views.SessionListView.as_view(), name='list_sessions'),
    path('delete_schedule/<int:pk>/', views.SchedulerDeleteView.as_view(), name='delete_schedule'),
    path('mark_as_paid/<int:pk>/', views.MarkAsPaidView.as_view(), name='mark_as_paid'),
    path('payment_page/', views.PaymentPageView.as_view(), name='payment_page'),
    path('list_sessions/<int:pk>/', views.ProgressSessionView.as_view(), name='progress_session'),
]
