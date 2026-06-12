"""
News app sitemaps for SEO - Blog Posts
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from .models import Post, Category


class PostSitemap(Sitemap):
    """
    Sitemap for blog posts/news articles
    """
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return Post.objects.filter(
            is_published=True,
            published_at__lte=timezone.now()
        ).select_related('category')
    
    def location(self, obj):
        return reverse('news:post_detail', kwargs={'slug': obj.slug})
    
    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    """
    Sitemap for news categories
    """
    priority = 0.6
    changefreq = 'monthly'
    
    def items(self):
        return Category.objects.filter(is_active=True)
    
    def location(self, obj):
        return reverse('news:category_detail', kwargs={'slug': obj.slug})
    
    def lastmod(self, obj):
        # Use the latest post date in the category
        latest_post = obj.posts.filter(
            is_published=True,
            published_at__lte=timezone.now()
        ).order_by('-published_at').first()
        
        return latest_post.published_at if latest_post else None
