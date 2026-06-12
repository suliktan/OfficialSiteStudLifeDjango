"""
Geo app URL configuration with i18n support
"""
from django.urls import path
from . import views

app_name = 'geo'

urlpatterns = [
    path('', views.country_list, name='country_list'),
    path('<slug:slug>/', views.country_detail, name='country_detail'),
    path('<slug:country_slug>/<slug:slug>/', views.city_detail, name='city_detail'),
    path('api/cities/<slug:country_slug>/', views.get_cities_by_country, name='api_cities_by_country'),
]
