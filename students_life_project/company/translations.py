"""
Translation options for company app models using django-modeltranslation
"""
from modeltranslation.translator import translator, TranslationOptions
from .models import Office, Employee


class OfficeTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'address',
        'city',
        'working_hours',
    )


class EmployeeTranslationOptions(TranslationOptions):
    fields = (
        'first_name',
        'last_name',
        'full_name',
        'position',
        'department',
        'bio',
    )


# Register translation options
translator.register(Office, OfficeTranslationOptions)
translator.register(Employee, EmployeeTranslationOptions)
