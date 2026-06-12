"""
Company app models - Offices and Employees
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from filer.fields.image import FilerImageField


class Office(models.Model):
    """Office locations (7 offices)"""
    
    name = models.CharField(_('Office Name'), max_length=255)
    slug = models.SlugField(_('Slug'), unique=True, max_length=255)
    address = models.TextField(_('Address'), blank=True)
    city = models.CharField(_('City'), max_length=255, blank=True)
    country = models.CharField(_('Country'), max_length=255, blank=True)
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    working_hours = models.CharField(_('Working Hours'), max_length=255, blank=True, help_text=_('e.g., Mon-Fri 9:00-18:00'))
    
    # Media
    image = FilerImageField(
        verbose_name=_('Office Image'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='office_images'
    )
    
    # Settings
    is_active = models.BooleanField(_('Is Active'), default=True)
    order = models.PositiveIntegerField(_('Order'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Office')
        verbose_name_plural = _('Offices')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('company:office_detail', kwargs={'slug': self.slug})
    
    def get_employees_count(self):
        return self.employees.count()


class Employee(models.Model):
    """Employee profiles (25-30 people) linked to offices"""
    
    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name=_('Office')
    )
    
    # Personal Information
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    full_name = models.CharField(_('Full Name'), max_length=255, blank=True, help_text=_('Auto-generated if empty'))
    
    position = models.CharField(_('Position'), max_length=255)
    department = models.CharField(_('Department'), max_length=255, blank=True)
    bio = models.TextField(_('Biography'), blank=True)
    
    # Contact
    email = models.EmailField(_('Email'), blank=True)
    phone = models.CharField(_('Phone'), max_length=50, blank=True)
    
    # Social Media
    linkedin = models.URLField(_('LinkedIn'), blank=True)
    facebook = models.URLField(_('Facebook'), blank=True)
    instagram = models.URLField(_('Instagram'), blank=True)
    
    # Media
    photo = FilerImageField(
        verbose_name=_('Photo'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_photos'
    )
    
    # Settings
    is_published = models.BooleanField(_('Is Published'), default=True)
    is_featured = models.BooleanField(_('Is Featured'), default=False, help_text=_('Show on homepage team section'))
    order = models.PositiveIntegerField(_('Order'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['office', 'order', 'last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"
    
    def save(self, *args, **kwargs):
        # Auto-generate full_name if not provided
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('company:employee_detail', kwargs={'pk': self.pk})
