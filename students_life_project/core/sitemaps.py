"""
Core app sitemaps for SEO
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages (homepage, about, contact, etc.)
    """
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return ['core:home']
    
    def location(self, item):
        return reverse(item)


class DocumentSitemap(Sitemap):
    """
    Sitemap for public documents
    """
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        from .models import Document
        return Document.objects.filter(is_public=True)
    
    def location(self, obj):
        # Documents are displayed on homepage, no separate URL
        return reverse('core:home')
    
    def lastmod(self, obj):
        return obj.uploaded_at
