"""
Core app URL configuration
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/submit/', views.contact_form_submit, name='contact_submit'),
    path('consultation/submit/', views.consultation_form_submit, name='consultation_submit'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('consultation/success/', views.consultation_success, name='consultation_success'),
]
