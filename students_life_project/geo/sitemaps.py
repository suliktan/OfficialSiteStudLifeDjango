"""
Geo app sitemaps for SEO - Countries and Cities
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Country, City


class CountrySitemap(Sitemap):
    """
    Sitemap for country pages
    """
    priority = 0.9
    changefreq = 'monthly'
    
    def items(self):
        return Country.objects.filter(is_published=True)
    
    def location(self, obj):
        return reverse('geo:country_detail', kwargs={'slug': obj.slug})
    
    def lastmod(self, obj):
        return obj.updated_at


class CitySitemap(Sitemap):
    """
    Sitemap for city pages
    """
    priority = 0.7
    changefreq = 'monthly'
    
    def items(self):
        return City.objects.filter(is_published=True).select_related('country')
    
    def location(self, obj):
        return reverse('geo:city_detail', kwargs={
            'country_slug': obj.country.slug,
            'slug': obj.slug
        })
    
    def lastmod(self, obj):
        return obj.updated_at
