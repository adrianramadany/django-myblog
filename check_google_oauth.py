#!/usr/bin/env python
"""
Script untuk memeriksa dan memperbaiki konfigurasi Google OAuth
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp, SocialAccount

def check_google_oauth():
    print("=== Pemeriksaan Konfigurasi Google OAuth ===\n")
    
    # Check Site
    print("1. Memeriksa Site...")
    sites = Site.objects.all()
    if sites.exists():
        site = sites.first()
        print(f"   ✓ Site ditemukan: {site.name} (ID: {site.id})")
        print(f"   ✓ Domain: {site.domain}")
    else:
        print("   ✗ Tidak ada site yang ditemukan!")
        return False
    
    # Check SocialApp
    print("\n2. Memeriksa SocialApp...")
    social_apps = SocialApp.objects.filter(provider='google')
    if social_apps.exists():
        app = social_apps.first()
        print(f"   ✓ SocialApp ditemukan: {app.name}")
        print(f"   ✓ Provider: {app.provider}")
        print(f"   ✓ Client ID: {app.client_id[:20]}..." if app.client_id else "   ✗ Client ID kosong!")
        print(f"   ✓ Secret: {'***' if app.secret else '✗ Secret kosong!'}")
        
        # Check sites connection
        app_sites = app.sites.all()
        if app_sites.exists():
            print(f"   ✓ Terhubung ke {app_sites.count()} site(s)")
            for site in app_sites:
                print(f"     - {site.name} ({site.domain})")
        else:
            print("   ✗ SocialApp tidak terhubung ke site manapun!")
            print("   → Menghubungkan ke site...")
            app.sites.add(site)
            print("   ✓ Berhasil dihubungkan!")
    else:
        print("   ✗ Tidak ada SocialApp Google yang ditemukan!")
        return False
    
    # Check Provider
    print("\n3. Memeriksa Provider...")
    try:
        from allauth.socialaccount.providers.google.provider import GoogleProvider
        provider = GoogleProvider()
        print("   ✓ GoogleProvider berhasil diimpor")
    except Exception as e:
        print(f"   ✗ Error dengan GoogleProvider: {e}")
        return False
    
    print("\n=== Hasil Pemeriksaan ===")
    print("✓ Konfigurasi Google OAuth sudah benar!")
    print("✓ Tombol Google seharusnya muncul di halaman login")
    return True

if __name__ == "__main__":
    check_google_oauth() 