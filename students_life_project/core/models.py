"""
Core app models - Homepage content, testimonials, documents
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField


class SiteSetting(models.Model):
    """Global site settings managed via Django Admin"""
    
    site_name = models.CharField(_('Site Name'), max_length=255, default='Students Life')
    site_description = models.TextField(_('Site Description'), blank=True)
    contact_email = models.EmailField(_('Contact Email'), blank=True)
    contact_phone = models.CharField(_('Contact Phone'), max_length=50, blank=True)
    social_media_links = models.JSONField(_('Social Media Links'), default=dict, blank=True, help_text=_('JSON format: {"facebook": "url", "instagram": "url"}'))
    
    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')
    
    def __str__(self):
        return self.site_name


class Document(models.Model):
    """Official documents/contracts for the homepage section"""
    
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    file = FilerFileField(
        verbose_name=_('File'),
        on_delete=models.CASCADE,
        related_name='documents',
        help_text=_('Upload PDF or document file')
    )
    uploaded_at = models.DateTimeField(_('Uploaded At'), auto_now_add=True)
    is_public = models.BooleanField(_('Is Public'), default=True)
    order = models.PositiveIntegerField(_('Order'), default=0, help_text=_('Display order'))
    
    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['order', 'uploaded_at']
    
    def __str__(self):
        return self.title


class TestimonialType(models.TextChoices):
    VIDEO = 'video', _('Video')
    TEXT = 'text', _('Text Message')


class Testimonial(models.Model):
    """Testimonials section - video and text reviews"""
    
    testimonial_type = models.CharField(
        _('Type'),
        max_length=10,
        choices=TestimonialType.choices,
        default=TestimonialType.TEXT
    )
    author_name = models.CharField(_('Author Name'), max_length=255)
    author_photo = FilerImageField(
        verbose_name=_('Author Photo'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonial_photos'
    )
    content = models.TextField(_('Content'), help_text=_('Text content for text testimonials'))
    video_url = models.CharField(_('Video URL'), max_length=500, blank=True, help_text=_('YouTube/Vimeo URL for video testimonials'))
    country = models.CharField(_('Country'), max_length=100, blank=True, help_text=_('Country where student studied'))
    university = models.CharField(_('University'), max_length=255, blank=True)
    is_featured = models.BooleanField(_('Is Featured'), default=False, help_text=_('Show on homepage'))
    is_published = models.BooleanField(_('Is Published'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    order = models.PositiveIntegerField(_('Order'), default=0)
    
    class Meta:
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.author_name} - {self.get_testimonial_type_display()}"


class AboutSection(models.Model):
    """About company section content"""
    
    title = models.CharField(_('Title'), max_length=255)
    content = models.TextField(_('Content'))
    image = FilerImageField(
        verbose_name=_('Image'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='about_images'
    )
    order = models.PositiveIntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)
    
    class Meta:
        verbose_name = _('About Section')
        verbose_name_plural = _('About Sections')
        ordering = ['order']
    
    def __str__(self):
        return self.title
