"""
Translation options for news app models using django-modeltranslation
"""
from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Tag, Post


class CategoryTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
        'meta_title',
        'meta_description',
    )


class TagTranslationOptions(TranslationOptions):
    # Tags typically don't need translation, but can be added if needed
    pass


class PostTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'subtitle',
        'excerpt',
        'content',
        'meta_title',
        'meta_description',
        'meta_keywords',
        'author',
    )


# Register translation options
translator.register(Category, CategoryTranslationOptions)
translator.register(Tag, TagTranslationOptions)
translator.register(Post, PostTranslationOptions)
