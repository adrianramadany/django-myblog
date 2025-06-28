from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import Article, Category, Gallery, UserProfile
from .forms import ArticleForm, CategoryForm, GalleryForm, UserProfileForm

def is_admin_or_author(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name__in=['Admin', 'Author']).exists())

def home(request):
    """Landing page dengan daftar artikel terbaru"""
    latest_articles = Article.objects.filter(status='published').order_by('-published_at')[:6]
    categories = Category.objects.annotate(article_count=Count('articles')).order_by('-article_count')[:5]
    featured_articles = Article.objects.filter(status='published').order_by('-views')[:3]
    
    context = {
        'latest_articles': latest_articles,
        'categories': categories,
        'featured_articles': featured_articles,
    }
    return render(request, 'blog/home.html', context)

def about(request):
    """Halaman About/CV"""
    return render(request, 'blog/about.html')

def article_list(request):
    """Daftar semua artikel"""
    articles = Article.objects.filter(status='published').order_by('-published_at')
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')
    
    if category_filter:
        articles = articles.filter(category__slug=category_filter)
    
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query,
    }
    return render(request, 'blog/article_list.html', context)

def article_detail(request, slug):
    """Detail artikel"""
    article = get_object_or_404(Article, slug=slug, status='published')
    article.views += 1
    article.save()
    
    # Artikel terkait
    related_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(id=article.id).order_by('-published_at')[:3]
    
    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'blog/article_detail.html', context)

def category_detail(request, slug):
    """Detail kategori"""
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category, status='published').order_by('-published_at')
    
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_detail.html', context)

def register(request):
    """Halaman registrasi"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Tambahkan ke group Author secara default
            author_group, created = Group.objects.get_or_create(name='Author')
            user.groups.add(author_group)
            
            # Buat UserProfile
            UserProfile.objects.create(user=user)
            
            messages.success(request, 'Registrasi berhasil! Silakan login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_author)
def dashboard(request):
    """Dashboard untuk admin dan author"""
    # Statistik
    total_articles = Article.objects.count()
    published_articles = Article.objects.filter(status='published').count()
    draft_articles = Article.objects.filter(status='draft').count()
    total_categories = Category.objects.count()
    total_users = User.objects.count()
    
    # Artikel terbaru
    recent_articles = Article.objects.order_by('-created_at')[:5]
    
    # Statistik per kategori
    category_stats = Category.objects.annotate(
        article_count=Count('articles')
    ).order_by('-article_count')[:5]
    
    # Statistik per user
    user_stats = User.objects.annotate(
        article_count=Count('articles')
    ).filter(article_count__gt=0).order_by('-article_count')[:5]
    
    # Grafik data untuk Chart.js
    chart_data = {
        'categories': [cat.name for cat in category_stats],
        'article_counts': [cat.article_count for cat in category_stats],
    }
    
    context = {
        'total_articles': total_articles,
        'published_articles': published_articles,
        'draft_articles': draft_articles,
        'total_categories': total_categories,
        'total_users': total_users,
        'recent_articles': recent_articles,
        'category_stats': category_stats,
        'user_stats': user_stats,
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'blog/dashboard.html', context)

# CRUD Operations untuk Article
@login_required
@user_passes_test(is_admin_or_author)
def article_create(request):
    """Buat artikel baru"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, 'Artikel berhasil dibuat!')
            return redirect('article_list')
    else:
        form = ArticleForm()
    
    return render(request, 'blog/article_form.html', {'form': form, 'title': 'Buat Artikel Baru'})

@login_required
@user_passes_test(is_admin_or_author)
def article_update(request, pk):
    """Update artikel"""
    article = get_object_or_404(Article, pk=pk)
    
    # Hanya author atau admin yang bisa edit
    if not (request.user.is_staff or article.author == request.user):
        messages.error(request, 'Anda tidak memiliki izin untuk mengedit artikel ini.')
        return redirect('article_list')
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artikel berhasil diperbarui!')
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'blog/article_form.html', {'form': form, 'title': 'Edit Artikel'})

@login_required
@user_passes_test(is_admin_or_author)
def article_delete(request, pk):
    """Hapus artikel"""
    article = get_object_or_404(Article, pk=pk)
    
    # Hanya author atau admin yang bisa hapus
    if not (request.user.is_staff or article.author == request.user):
        messages.error(request, 'Anda tidak memiliki izin untuk menghapus artikel ini.')
        return redirect('article_list')
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Artikel berhasil dihapus!')
        return redirect('article_list')
    
    return render(request, 'blog/article_confirm_delete.html', {'article': article})

# CRUD Operations untuk Category
@login_required
@user_passes_test(is_admin_or_author)
def category_list(request):
    """Daftar kategori"""
    categories = Category.objects.annotate(article_count=Count('articles')).order_by('name')
    return render(request, 'blog/category_list.html', {'categories': categories})

@login_required
@user_passes_test(is_admin_or_author)
def category_create(request):
    """Buat kategori baru"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori berhasil dibuat!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'blog/category_form.html', {'form': form, 'title': 'Buat Kategori Baru'})

@login_required
@user_passes_test(is_admin_or_author)
def category_update(request, pk):
    """Update kategori"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori berhasil diperbarui!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'blog/category_form.html', {'form': form, 'title': 'Edit Kategori'})

@login_required
@user_passes_test(is_admin_or_author)
def category_delete(request, pk):
    """Hapus kategori"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategori berhasil dihapus!')
        return redirect('category_list')
    
    return render(request, 'blog/category_confirm_delete.html', {'category': category})

# CRUD Operations untuk Gallery
@login_required
@user_passes_test(is_admin_or_author)
def gallery_list(request):
    """Daftar galeri"""
    galleries = Gallery.objects.all().order_by('-created_at')
    # Filter hanya gallery yang memiliki gambar
    galleries = [gallery for gallery in galleries if gallery.image]
    return render(request, 'blog/gallery_list.html', {'galleries': galleries})

@login_required
@user_passes_test(is_admin_or_author)
def gallery_create(request):
    """Buat galeri baru"""
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Galeri berhasil dibuat!')
            return redirect('gallery_list')
    else:
        form = GalleryForm()
    
    return render(request, 'blog/gallery_form.html', {'form': form, 'title': 'Buat Galeri Baru'})

@login_required
@user_passes_test(is_admin_or_author)
def gallery_update(request, pk):
    """Update galeri"""
    gallery = get_object_or_404(Gallery, pk=pk)
    
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=gallery)
        if form.is_valid():
            form.save()
            messages.success(request, 'Galeri berhasil diperbarui!')
            return redirect('gallery_list')
    else:
        form = GalleryForm(instance=gallery)
    
    return render(request, 'blog/gallery_form.html', {'form': form, 'title': 'Edit Galeri'})

@login_required
@user_passes_test(is_admin_or_author)
def gallery_delete(request, pk):
    """Hapus galeri"""
    gallery = get_object_or_404(Gallery, pk=pk)
    
    if request.method == 'POST':
        gallery.delete()
        messages.success(request, 'Galeri berhasil dihapus!')
        return redirect('gallery_list')
    
    return render(request, 'blog/gallery_confirm_delete.html', {'gallery': gallery})

# User Management
@login_required
@user_passes_test(lambda u: u.is_staff)
def user_list(request):
    """Daftar user (hanya untuk admin)"""
    users = User.objects.all().order_by('username')
    return render(request, 'blog/user_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_staff)
def user_update(request, pk):
    """Update user (hanya untuk admin)"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        # Update groups
        groups = request.POST.getlist('groups')
        user.groups.clear()
        for group_id in groups:
            group = Group.objects.get(id=group_id)
            user.groups.add(group)
        
        # Update is_staff
        user.is_staff = 'is_staff' in request.POST
        user.save()
        
        messages.success(request, 'User berhasil diperbarui!')
        return redirect('user_list')
    
    groups = Group.objects.all()
    return render(request, 'blog/user_form.html', {'user': user, 'groups': groups})

@login_required
def profile_update(request):
    """Update profil user"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'blog/profile_form.html', {'form': form})
