from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('articles/', views.article_list, name='article_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Article CRUD - Pindahkan create sebelum detail
    path('article/create/', views.article_create, name='article_create'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('article/<int:pk>/edit/', views.article_update, name='article_update'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),
    
    # Category CRUD
    path('categories/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:pk>/edit/', views.category_update, name='category_update'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Gallery CRUD
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/create/', views.gallery_create, name='gallery_create'),
    path('gallery/<int:pk>/edit/', views.gallery_update, name='gallery_update'),
    path('gallery/<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),
    
    # User Management
    path('users/', views.user_list, name='user_list'),
    path('user/<int:pk>/edit/', views.user_update, name='user_update'),
    path('profile/edit/', views.profile_update, name='profile_update'),
] 