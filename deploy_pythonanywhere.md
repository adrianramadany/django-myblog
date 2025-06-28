# Panduan Deployment MyBlog ke PythonAnywhere

## 📋 Persiapan

### 1. Akun PythonAnywhere
- Daftar akun gratis di [PythonAnywhere](https://www.pythonanywhere.com)
- Pilih plan yang sesuai (Free plan cukup untuk testing)

### 2. File Project
- Pastikan semua file project sudah siap
- Struktur folder harus lengkap

## 🚀 Langkah Deployment

### 1. Upload Files
1. Login ke PythonAnywhere
2. Buka **Files** tab
3. Buat folder baru: `myblog`
4. Upload semua file project ke folder tersebut
5. Pastikan struktur folder seperti ini:
   ```
   myblog/
   ├── blog/
   ├── myblog/
   ├── templates/
   ├── static/
   ├── media/
   ├── manage.py
   ├── requirements.txt
   └── README.md
   ```

### 2. Setup Virtual Environment
1. Buka **Consoles** tab
2. Pilih **Bash** console
3. Navigasi ke folder project:
   ```bash
   cd myblog
   ```
4. Buat virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 myblog
   ```
5. Aktifkan virtual environment:
   ```bash
   workon myblog
   ```
6. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Database Setup
1. Dalam virtual environment, jalankan:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Buat superuser:
   ```bash
   python manage.py createsuperuser
   ```

### 4. Static Files
1. Jalankan collectstatic:
   ```bash
   python manage.py collectstatic
   ```

### 5. Configure Web App
1. Buka **Web** tab
2. Klik **Add a new web app**
3. Pilih **Manual configuration**
4. Pilih **Python 3.9**
5. Set **Source code** ke: `/home/username/myblog`
6. Set **Working directory** ke: `/home/username/myblog`

### 6. Configure WSGI File
1. Klik **WSGI configuration file**
2. Edit file dan ganti dengan kode berikut:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/username/myblog'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'myblog.settings'

# Activate virtual environment
activate_this = '/home/username/.virtualenvs/myblog/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Catatan**: Ganti `username` dengan username PythonAnywhere Anda.

### 7. Configure Settings
1. Edit file `myblog/settings.py`
2. Ubah konfigurasi untuk production:

```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['username.pythonanywhere.com']

# Static files
STATIC_ROOT = '/home/username/myblog/staticfiles'
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = '/home/username/myblog/media'
MEDIA_URL = '/media/'

# Security
SECRET_KEY = 'your-secret-key-here'
```

### 8. Configure URLs
1. Edit file `myblog/urls.py`
2. Tambahkan konfigurasi untuk static dan media files:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... existing patterns ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 9. Reload Web App
1. Kembali ke **Web** tab
2. Klik **Reload** button
3. Tunggu beberapa saat sampai reload selesai

## 🔧 Troubleshooting

### Error: ModuleNotFoundError
- Pastikan virtual environment aktif
- Check path di WSGI file
- Restart web app

### Error: Static files not found
- Jalankan `python manage.py collectstatic`
- Check STATIC_ROOT path
- Reload web app

### Error: Database errors
- Check database settings
- Run migrations: `python manage.py migrate`
- Check file permissions

### Error: Media files not uploading
- Check MEDIA_ROOT path
- Ensure directory exists and writable
- Check file permissions

## 📊 Monitoring

### Logs
- Check **Web** tab untuk error logs
- Monitor **Files** untuk disk usage
- Check **Tasks** untuk background jobs

### Performance
- Monitor CPU usage
- Check memory usage
- Optimize database queries

## 🔒 Security

### Production Checklist
- [ ] DEBUG = False
- [ ] Secret key changed
- [ ] Allowed hosts configured
- [ ] HTTPS enabled (paid plan)
- [ ] Database secured
- [ ] Static files served properly

### Backup
- Regular database backups
- File system backups
- Code version control

## 🌐 Domain Configuration

### Custom Domain (Paid Plan)
1. Add custom domain in **Web** tab
2. Configure DNS settings
3. Update ALLOWED_HOSTS
4. Reload web app

### SSL Certificate
1. Enable HTTPS in **Web** tab
2. Configure SSL certificate
3. Update settings for HTTPS

## 📈 Scaling

### Performance Optimization
- Enable caching
- Optimize database queries
- Use CDN for static files
- Enable compression

### Monitoring Tools
- PythonAnywhere analytics
- Django debug toolbar (development)
- Database query monitoring

## 🎯 Final Steps

1. **Test all features**:
   - User registration/login
   - Article CRUD
   - Admin panel
   - File uploads
   - Search functionality

2. **SEO Optimization**:
   - Meta tags
   - Sitemap
   - Robots.txt
   - Schema markup

3. **Documentation**:
   - Update README.md
   - Create user guide
   - Document API (if any)

4. **Backup**:
   - Database backup
   - File system backup
   - Configuration backup

## 📞 Support

Jika mengalami masalah:
1. Check PythonAnywhere documentation
2. Review Django deployment guide
3. Check error logs
4. Contact PythonAnywhere support

---

**MyBlog** - Successfully deployed on PythonAnywhere! 🚀 