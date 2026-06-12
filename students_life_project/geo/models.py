"""
Geo app models - Countries and Cities with SEO fields
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from filer.fields.image import FilerImageField


class Country(models.Model):
    """Country model with SEO fields and translations"""
    
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), unique=True, max_length=255, help_text=_('URL-friendly name'))
    description = models.TextField(_('Description'), blank=True)
    
    # SEO Fields
    meta_title = models.CharField(_('Meta Title'), max_length=255, blank=True, help_text=_('SEO title for search engines'))
    meta_description = models.TextField(_('Meta Description'), blank=True, help_text=_('SEO description for search engines'))
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=500, blank=True, help_text=_('Comma-separated keywords'))
    
    # Media
    flag = FilerImageField(
        verbose_name=_('Flag'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='country_flags'
    )
    cover_image = FilerImageField(
        verbose_name=_('Cover Image'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='country_covers'
    )
    
    # Settings
    is_published = models.BooleanField(_('Is Published'), default=True)
    order = models.PositiveIntegerField(_('Order'), default=0, help_text=_('Display order in lists'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('geo:country_detail', kwargs={'slug': self.slug})
    
    def get_cities_count(self):
        return self.cities.count()


class City(models.Model):
    """City model linked to Country with SEO fields and translations"""
    
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cities',
        verbose_name=_('Country')
    )
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, help_text=_('URL-friendly name'))
    description = models.TextField(_('Description'), blank=True)
    
    # Student-specific information
    student_info = models.TextField(_('Student Information'), blank=True, help_text=_('Information specifically for students'))
    universities_count = models.PositiveIntegerField(_('Universities Count'), default=0, blank=True, null=True)
    average_cost = models.CharField(_('Average Cost'), max_length=100, blank=True, help_text=_('Average living/education cost'))
    
    # SEO Fields
    meta_title = models.CharField(_('Meta Title'), max_length=255, blank=True)
    meta_description = models.TextField(_('Meta Description'), blank=True)
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=500, blank=True)
    
    # Media
    image = FilerImageField(
        verbose_name=_('Image'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='city_images'
    )
    
    # Settings
    is_published = models.BooleanField(_('Is Published'), default=True)
    order = models.PositiveIntegerField(_('Order'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        ordering = ['country', 'order', 'name']
        unique_together = [['country', 'slug']]
    
    def __str__(self):
        return f"{self.name}, {self.country.name}"
    
    def get_absolute_url(self):
        return reverse('geo:city_detail', kwargs={'country_slug': self.country.slug, 'slug': self.slug})
