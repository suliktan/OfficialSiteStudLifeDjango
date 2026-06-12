"""
News app views - Blog/News with filtering and SEO
"""
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Post, Category, Tag


def post_list(request):
    """
    List all published news/blog posts.
    URL: /news/ or /en/news/
    
    Supports filtering by category, tag, and year/month.
    """
    # Get only published posts that are not in the future
    posts = Post.objects.filter(
        is_published=True,
        published_at__lte=timezone.now()
    ).select_related('category', 'featured_image').prefetch_related('tags').order_by('-published_at', '-created_at')
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Filter by tag if provided
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Filter by year/month if provided
    year = request.GET.get('year')
    month = request.GET.get('month')
    if year:
        posts = posts.filter(published_at__year=year)
        if month:
            posts = posts.filter(published_at__month=month)
    
    # Get featured posts for sidebar
    featured_posts = Post.objects.filter(
        is_published=True,
        is_featured=True,
        published_at__lte=timezone.now()
    ).select_related('featured_image').order_by('-published_at')[:5]
    
    # Get active categories
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    
    # Pagination
    paginator = Paginator(posts, 12)  # 12 posts per page
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    context = {
        'page_obj': page_obj,
        'featured_posts': featured_posts,
        'categories': categories,
        'page_title': _('News & Articles'),
        'current_category': category_slug,
        'current_tag': tag_slug,
    }
    
    return render(request, 'news/post_list.html', context)


def post_detail(request, slug):
    """
    Display individual blog post/news article.
    URL: /news/<slug>/ or /en/news/<slug>/
    
    Includes SEO meta tags and related posts.
    """
    post = get_object_or_404(
        Post.objects.select_related('category', 'featured_image', 'author').prefetch_related('tags', 'gallery'),
        slug=slug,
        is_published=True,
        published_at__lte=timezone.now()
    )
    
    # Increment view count
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    # Get related posts (same category or tags)
    related_posts = Post.objects.filter(
        is_published=True,
        published_at__lte=timezone.now()
    ).filter(
        models.Q(category=post.category) | models.Q(tags__in=post.tags.all())
    ).exclude(pk=post.pk).select_related('featured_image').distinct()[:4]
    
    # Build SEO meta tags
    meta_title = post.meta_title or post.title
    meta_description = post.meta_description or post.excerpt or post.content[:160]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'page_title': post.title,
        'meta_title': meta_title,
        'meta_description': meta_description,
        'meta_keywords': post.meta_keywords,
    }
    
    return render(request, 'news/post_detail.html', context)


def category_detail(request, slug):
    """
    Display posts in a specific category.
    URL: /news/category/<slug>/ or /en/news/category/<slug>/
    """
    category = get_object_or_404(
        Category.objects.filter(is_active=True),
        slug=slug
    )
    
    posts = Post.objects.filter(
        is_published=True,
        category=category,
        published_at__lte=timezone.now()
    ).select_related('featured_image').order_by('-published_at')
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    # Build SEO meta tags
    meta_title = category.meta_title or category.name
    meta_description = category.meta_description or category.description[:160] if category.description else ''
    
    context = {
        'page_obj': page_obj,
        'category': category,
        'page_title': category.name,
        'meta_title': meta_title,
        'meta_description': meta_description,
    }
    
    return render(request, 'news/category_detail.html', context)


def tag_detail(request, slug):
    """
    Display posts with a specific tag.
    URL: /news/tag/<slug>/ or /en/news/tag/<slug>/
    """
    tag = get_object_or_404(Tag, slug=slug)
    
    posts = Post.objects.filter(
        is_published=True,
        tags=tag,
        published_at__lte=timezone.now()
    ).select_related('featured_image').order_by('-published_at')
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    context = {
        'page_obj': page_obj,
        'tag': tag,
        'page_title': f'{_("Posts tagged")} "{tag.name}"',
    }
    
    return render(request, 'news/tag_detail.html', context)


# Import models for related_posts query
from django.db import models
