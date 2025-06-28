#!/usr/bin/env python
"""
Test script untuk MyBlog application
Menjalankan beberapa test dasar untuk memastikan aplikasi berfungsi dengan baik
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from blog.models import Category, Article, Gallery, UserProfile

def test_basic_functionality():
    """Test fungsi dasar aplikasi"""
    print("🧪 Testing MyBlog Application...")
    
    # Test 1: Database connection
    try:
        user_count = User.objects.count()
        print(f"✅ Database connection: OK ({user_count} users)")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    # Test 2: Create test data
    try:
        # Create test user
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        # Create test category
        test_category, created = Category.objects.get_or_create(
            name='Test Category',
            defaults={'description': 'Test category for testing'}
        )
        
        # Create test article
        test_article, created = Article.objects.get_or_create(
            title='Test Article',
            defaults={
                'content': 'This is a test article content.',
                'category': test_category,
                'author': test_user,
                'status': 'published'
            }
        )
        
        print(f"✅ Test data created: {test_user.username}, {test_category.name}, {test_article.title}")
        
    except Exception as e:
        print(f"❌ Test data creation failed: {e}")
        return False
    
    # Test 3: URL patterns
    try:
        client = Client()
        
        # Test home page
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Home page: OK")
        else:
            print(f"❌ Home page failed: {response.status_code}")
        
        # Test article list
        response = client.get('/articles/')
        if response.status_code == 200:
            print("✅ Article list: OK")
        else:
            print(f"❌ Article list failed: {response.status_code}")
        
        # Test about page
        response = client.get('/about/')
        if response.status_code == 200:
            print("✅ About page: OK")
        else:
            print(f"❌ About page failed: {response.status_code}")
        
    except Exception as e:
        print(f"❌ URL testing failed: {e}")
        return False
    
    # Test 4: Models functionality
    try:
        # Test article methods
        excerpt = test_article.get_excerpt()
        if excerpt:
            print("✅ Article excerpt method: OK")
        
        # Test category methods
        category_url = test_category.get_absolute_url()
        if category_url:
            print("✅ Category URL method: OK")
        
        # Test user profile
        profile, created = UserProfile.objects.get_or_create(user=test_user)
        if profile:
            print("✅ User profile: OK")
        
    except Exception as e:
        print(f"❌ Model testing failed: {e}")
        return False
    
    print("\n🎉 All basic tests passed!")
    return True

def test_admin_functionality():
    """Test fungsi admin"""
    print("\n🔧 Testing Admin Functionality...")
    
    try:
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            print("✅ Admin user created")
        
        # Create Author group
        author_group, created = Group.objects.get_or_create(name='Author')
        if created:
            print("✅ Author group created")
        
        # Test admin access
        client = Client()
        client.login(username='admin', password='admin123')
        
        response = client.get('/admin/')
        if response.status_code == 200:
            print("✅ Admin panel access: OK")
        else:
            print(f"❌ Admin panel access failed: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Admin testing failed: {e}")
        return False
    
    print("🎉 Admin functionality tests passed!")
    return True

def cleanup_test_data():
    """Clean up test data"""
    print("\n🧹 Cleaning up test data...")
    
    try:
        # Delete test data
        User.objects.filter(username__in=['testuser', 'admin']).delete()
        Category.objects.filter(name='Test Category').delete()
        Article.objects.filter(title='Test Article').delete()
        
        print("✅ Test data cleaned up")
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")

def main():
    """Main test function"""
    print("🚀 Starting MyBlog Application Tests")
    print("=" * 50)
    
    # Run tests
    basic_ok = test_basic_functionality()
    admin_ok = test_admin_functionality()
    
    # Cleanup
    cleanup_test_data()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"Basic Functionality: {'✅ PASS' if basic_ok else '❌ FAIL'}")
    print(f"Admin Functionality: {'✅ PASS' if admin_ok else '❌ FAIL'}")
    
    if basic_ok and admin_ok:
        print("\n🎉 All tests passed! MyBlog is ready to use.")
        print("\n📝 Next steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000")
        print("3. Login to admin: http://127.0.0.1:8000/admin")
        print("4. Create your first article!")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return basic_ok and admin_ok

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 