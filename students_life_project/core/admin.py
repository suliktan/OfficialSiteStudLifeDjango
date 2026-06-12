"""
Core app admin configuration
"""
from django.contrib import admin
from .models import SiteSetting, Document, Testimonial, AboutSection


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'contact_email', 'contact_phone']
    readonly_fields = []
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_description')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Social Media', {
            'fields': ('social_media_links',),
            'description': 'Enter as JSON: {"facebook": "url", "instagram": "url"}'
        }),
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_public', 'order', 'uploaded_at']
    list_filter = ['is_public', 'uploaded_at']
    search_fields = ['title', 'description']
    ordering = ['order', 'uploaded_at']
    
    fieldsets = (
        ('Document Info', {
            'fields': ('title', 'description', 'file')
        }),
        ('Settings', {
            'fields': ('is_public', 'order')
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'testimonial_type', 'country', 'is_featured', 'is_published', 'created_at']
    list_filter = ['testimonial_type', 'is_featured', 'is_published', 'created_at']
    search_fields = ['author_name', 'content', 'country', 'university']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('testimonial_type', 'author_name', 'author_photo')
        }),
        ('Content', {
            'fields': ('content', 'video_url')
        }),
        ('Context', {
            'fields': ('country', 'university')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_published', 'order')
        }),
    )


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'content']
    ordering = ['order']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'image')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )
