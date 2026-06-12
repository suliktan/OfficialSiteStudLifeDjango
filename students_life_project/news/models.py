"""
News app models - Blog/News posts with SEO and publication status
"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from filer.fields.image import FilerImageField


class Category(models.Model):
    """News/Blog categories"""
    
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True, max_length=100)
    description = models.TextField(_('Description'), blank=True)
    
    # SEO Fields
    meta_title = models.CharField(_('Meta Title'), max_length=255, blank=True)
    meta_description = models.TextField(_('Meta Description'), blank=True)
    
    order = models.PositiveIntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('news:category_detail', kwargs={'slug': self.slug})
    
    def get_posts_count(self):
        return self.posts.filter(is_published=True, published_at__lte=timezone.now()).count()


class Tag(models.Model):
    """Tags for news posts"""
    
    name = models.CharField(_('Name'), max_length=50)
    slug = models.SlugField(_('Slug'), unique=True, max_length=50)
    
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class PostStatus(models.TextChoices):
    DRAFT = 'draft', _('Draft')
    PUBLISHED = 'published', _('Published')
    ARCHIVED = 'archived', _('Archived')


class Post(models.Model):
    """News/Blog posts with SEO fields and translations"""
    
    # Basic Information
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), unique=True, max_length=255, help_text=_('URL-friendly title'))
    subtitle = models.CharField(_('Subtitle'), max_length=500, blank=True, help_text=_('Short description or teaser'))
    
    # Content
    excerpt = models.TextField(_('Excerpt'), blank=True, help_text=_('Short summary for listings'))
    content = models.TextField(_('Content'), help_text=_('Main article content (HTML allowed)'))
    
    # SEO Fields
    meta_title = models.CharField(_('Meta Title'), max_length=255, blank=True, help_text=_('SEO title (defaults to title if empty)'))
    meta_description = models.TextField(_('Meta Description'), blank=True, help_text=_('SEO description for search engines'))
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=500, blank=True, help_text=_('Comma-separated keywords'))
    
    # Media
    featured_image = FilerImageField(
        verbose_name=_('Featured Image'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='post_featured_images'
    )
    gallery = models.ManyToManyField(
        'filer.Image',
        verbose_name=_('Gallery Images'),
        blank=True,
        related_name='post_galleries',
        help_text=_('Additional images for the post')
    )
    
    # Categorization
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name=_('Category')
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'),
        blank=True,
        related_name='posts',
        help_text=_('Hold Ctrl/Cmd to select multiple tags')
    )
    
    # Author
    author = models.CharField(_('Author'), max_length=255, blank=True, help_text=_('Author name (or select from employees)'))
    
    # Publication Settings
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=PostStatus.choices,
        default=PostStatus.DRAFT
    )
    is_published = models.BooleanField(_('Is Published'), default=False, help_text=_('Check to publish'))
    published_at = models.DateTimeField(
        _('Published At'),
        blank=True,
        null=True,
        help_text=_('Leave empty to auto-set on first publish')
    )
    is_featured = models.BooleanField(_('Is Featured'), default=False, help_text=_('Show on homepage'))
    
    # Engagement
    views_count = models.PositiveIntegerField(_('Views Count'), default=0, editable=False)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status', '-published_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news:post_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Auto-set published_at on first publish
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
            self.status = PostStatus.PUBLISHED
        elif not self.is_published:
            self.status = PostStatus.DRAFT
            self.published_at = None
        
        # Auto-generate meta_title if empty
        if not self.meta_title:
            self.meta_title = self.title
        
        super().save(*args, **kwargs)
    
    def is_published_now(self):
        """Check if post should be visible now"""
        return (
            self.is_published and 
            self.published_at and 
            self.published_at <= timezone.now()
        )
