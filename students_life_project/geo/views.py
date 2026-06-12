"""
Geo app views - Countries and Cities with i18n support
"""
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from .models import Country, City


def country_list(request):
    """
    List all published countries.
    URL: /countries/ or /en/countries/
    """
    countries = Country.objects.filter(
        is_published=True
    ).select_related('flag').order_by('order', 'name')
    
    return render(request, 'geo/country_list.html', {
        'countries': countries,
        'page_title': _('Countries'),
    })


def country_detail(request, slug):
    """
    Display country detail page with cities list.
    URL: /countries/<slug>/ or /en/countries/<slug>/
    
    Handles i18n by using modeltranslation fields automatically.
    """
    country = get_object_or_404(
        Country.objects.select_related('flag', 'cover_image'),
        slug=slug,
        is_published=True
    )
    
    cities = country.cities.filter(
        is_published=True
    ).select_related('image').order_by('order', 'name')
    
    # Build SEO meta tags
    meta_title = country.meta_title or country.name
    meta_description = country.meta_description or country.description[:160] if country.description else ''
    
    context = {
        'country': country,
        'cities': cities,
        'page_title': country.name,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keywords': country.meta_keywords,
    }
    
    return render(request, 'geo/country_detail.html', context)


def city_detail(request, country_slug, slug):
    """
    Display city detail page.
    URL: /countries/<country_slug>/<slug>/ or /en/countries/<country_slug>/<slug>/
    
    Prevents 404 errors by checking country existence first.
    """
    # Get country first to ensure proper hierarchy
    country = get_object_or_404(
        Country.objects.filter(is_published=True),
        slug=country_slug
    )
    
    # Get city within the country
    city = get_object_or_404(
        City.objects.select_related('country', 'image').filter(country=country),
        slug=slug,
        is_published=True
    )
    
    # Build SEO meta tags
    meta_title = city.meta_title or f"{city.name}, {country.name}"
    meta_description = city.meta_description or city.description[:160] if city.description else ''
    
    context = {
        'city': city,
        'country': country,
        'page_title': city.name,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keywords': city.meta_keywords,
    }
    
    return render(request, 'geo/city_detail.html', context)


def get_cities_by_country(request, country_slug):
    """
    AJAX endpoint to get cities for a selected country.
    Returns JSON list of cities for dynamic form population.
    """
    try:
        country = Country.objects.get(slug=country_slug, is_published=True)
        cities = country.cities.filter(is_published=True).order_by('order', 'name')
        
        cities_data = [
            {'slug': city.slug, 'name': str(city)}
            for city in cities
        ]
        
        return JsonResponse({'success': True, 'cities': cities_data})
    except Country.DoesNotExist:
        return JsonResponse({'success': False, 'cities': []})


# Import JsonResponse here to avoid circular imports
from django.http import JsonResponse
