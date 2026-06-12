"""
Core app context processors and middleware
"""
from django.utils import translation
from .models import SiteSetting, Testimonial, Document, AboutSection


def site_settings(request):
    """
    Context processor to make site settings available in all templates.
    Provides global settings, testimonials, and documents.
    """
    current_language = translation.get_language()
    
    # Get or create default site settings
    try:
        settings = SiteSetting.objects.first()
    except Exception:
        settings = None
    
    # Get featured testimonials for homepage
    featured_testimonials = Testimonial.objects.filter(
        is_featured=True,
        is_published=True
    ).select_related('author_photo')[:6]
    
    # Get public documents
    documents = Document.objects.filter(
        is_public=True
    ).select_related('file')[:10]
    
    # Get about sections
    about_sections = AboutSection.objects.filter(
        is_active=True
    ).select_related('image').order_by('order')
    
    return {
        'site_settings': settings,
        'featured_testimonials': featured_testimonials,
        'documents': documents,
        'about_sections': about_sections,
        'current_language': current_language,
        'languages': [lang for lang_code, lang_name in getattr(request, 'LANGUAGES', [])],
    }
