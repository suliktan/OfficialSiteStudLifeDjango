"""
Company app URL configuration
"""
from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('', views.office_list, name='office_list'),
    path('<slug:slug>/', views.office_detail, name='office_detail'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
]
