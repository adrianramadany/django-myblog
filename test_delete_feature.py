#!/usr/bin/env python
"""
Test script untuk memverifikasi fitur delete artikel
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.auth.models import User, Group
from blog.models import Category, Article
from django.test import TestCase, Client
from django.urls import reverse

def test_delete_feature():
    """Test fitur delete artikel"""
    print("=== Testing Delete Article Feature ===")
    
    # Buat test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        print(f"✓ Created test user: {user.username}")
    
    # Buat group Author jika belum ada
    author_group, created = Group.objects.get_or_create(name='Author')
    if created:
        print("✓ Created Author group")
    
    # Tambahkan user ke group Author
    user.groups.add(author_group)
    print(f"✓ Added {user.username} to Author group")
    
    # Buat kategori test
    category, created = Category.objects.get_or_create(
        name='Test Category',
        defaults={'description': 'Test category for delete feature'}
    )
    if created:
        print(f"✓ Created test category: {category.name}")
    
    # Buat artikel test
    article, created = Article.objects.get_or_create(
        title='Test Article for Delete',
        defaults={
            'content': 'This is a test article for delete feature testing.',
            'author': user,
            'category': category,
            'status': 'published'
        }
    )
    if created:
        print(f"✓ Created test article: {article.title}")
    
    # Test client
    client = Client()
    
    # Login
    login_success = client.login(username='testuser', password='testpass123')
    if not login_success:
        # Set password jika belum
        user.set_password('testpass123')
        user.save()
        login_success = client.login(username='testuser', password='testpass123')
        print("✓ Set password and logged in")
    else:
        print("✓ Logged in successfully")
    
    # Test 1: Akses halaman delete
    delete_url = reverse('article_delete', kwargs={'pk': article.pk})
    response = client.get(delete_url)
    print(f"✓ GET delete page: {response.status_code}")
    
    # Test 2: Submit delete form
    response = client.post(delete_url)
    print(f"✓ POST delete: {response.status_code}")
    
    # Test 3: Verifikasi artikel sudah dihapus
    try:
        Article.objects.get(pk=article.pk)
        print("✗ Article still exists (should be deleted)")
    except Article.DoesNotExist:
        print("✓ Article successfully deleted")
    
    # Test 4: Verifikasi redirect ke dashboard
    if response.status_code == 302:
        print("✓ Redirected after delete")
        if 'dashboard' in response.url:
            print("✓ Redirected to dashboard")
        else:
            print(f"✗ Redirected to wrong URL: {response.url}")
    else:
        print(f"✗ No redirect, status: {response.status_code}")
    
    # Cleanup
    try:
        user.delete()
        print("✓ Cleaned up test user")
    except:
        pass
    
    try:
        category.delete()
        print("✓ Cleaned up test category")
    except:
        pass
    
    print("\n=== Delete Feature Test Complete ===")

if __name__ == '__main__':
    test_delete_feature() 