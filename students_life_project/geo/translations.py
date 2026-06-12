"""
Translation options for geo app models using django-modeltranslation
"""
from modeltranslation.translator import translator, TranslationOptions
from .models import Country, City


class CountryTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
        'meta_title',
        'meta_description',
        'meta_keywords',
    )


class CityTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
        'student_info',
        'average_cost',
        'meta_title',
        'meta_description',
        'meta_keywords',
    )


# Register translation options
translator.register(Country, CountryTranslationOptions)
translator.register(City, CityTranslationOptions)
