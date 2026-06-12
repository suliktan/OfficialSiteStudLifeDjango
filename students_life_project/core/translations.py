"""
Translation options for core app models using django-modeltranslation
"""
from modeltranslation.translator import translator, TranslationOptions
from .models import SiteSetting, Document, Testimonial, AboutSection


class SiteSettingTranslationOptions(TranslationOptions):
    fields = (
        'site_name',
        'site_description',
    )


class DocumentTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description',
    )


class TestimonialTranslationOptions(TranslationOptions):
    fields = (
        'author_name',
        'content',
        'country',
        'university',
    )


class AboutSectionTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'content',
    )


# Register translation options
translator.register(SiteSetting, SiteSettingTranslationOptions)
translator.register(Document, DocumentTranslationOptions)
translator.register(Testimonial, TestimonialTranslationOptions)
translator.register(AboutSection, AboutSectionTranslationOptions)
