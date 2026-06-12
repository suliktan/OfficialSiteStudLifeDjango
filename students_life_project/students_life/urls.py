"""
Django URL Configuration for Students Life Project
Includes i18n patterns for multilingual support
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Sitemap imports
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap
from geo.sitemaps import CountrySitemap, CitySitemap
from news.sitemaps import PostSitemap

# Define sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'countries': CountrySitemap,
    'cities': CitySitemap,
    'posts': PostSitemap,
}

# URLs that should NOT be prefixed with language code
urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Django Filer (media library)
    path('filer/', include('filer.urls')),
    
    # Sitemap.xml - available in all languages
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Robots.txt
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    
    # i18n JavaScript for frontend translations
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs with language prefix for i18n support
# This ensures URLs like /ru/countries/russia/ and /en/countries/russia/ work correctly
urlpatterns += i18n_patterns(
    # Core app (Homepage, forms)
    path('', include('core.urls')),
    
    # Geo app (Countries, Cities)
    path('countries/', include('geo.urls')),
    
    # Company app (Offices, Employees/Team)
    path('team/', include('company.urls')),
    
    # News app (Blog/Articles)
    path('news/', include('news.urls')),
    
    prefix_default_language=True  # Default language also gets prefix (/ru/...)
)

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error pages
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
