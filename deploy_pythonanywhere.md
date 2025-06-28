# Panduan Deployment Django ke PythonAnywhere

## Langkah 1: Persiapan Project

### 1.1 Update requirements.txt
Pastikan semua dependencies tercantum:
```
Django==5.2.3
Pillow==11.2.1
asgiref==3.8.1
sqlparse==0.5.3
django-allauth==0.60.1
django-crispy-forms==2.1
crispy-bootstrap5==0.7
python-decouple==3.8
django-ckeditor-5==0.2.18
whitenoise==6.6.0
gunicorn==21.2.0
```

### 1.2 Buat file .env untuk production
Buat file `.env` di root project:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DATABASE_URL=sqlite:///db.sqlite3
```

### 1.3 Update settings.py untuk production
Tambahkan konfigurasi production di settings.py

## Langkah 2: Daftar PythonAnywhere

1. Kunjungi [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Daftar akun gratis (Beginner plan)
3. Verifikasi email

## Langkah 3: Upload Project

### 3.1 Upload via Git (Recommended)
```bash
# Di local computer
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/myblog.git
git push -u origin main
```

### 3.2 Upload via Files
1. Buka Files tab di PythonAnywhere
2. Upload semua file project ke folder `/home/yourusername/`

## Langkah 4: Setup Virtual Environment

1. Buka Bash console di PythonAnywhere
2. Buat virtual environment:
```bash
cd /home/yourusername/
python3.11 -m venv myblog_env
source myblog_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Langkah 5: Setup Database

1. Jalankan migrations:
```bash
python manage.py migrate
```

2. Buat superuser:
```bash
python manage.py createsuperuser
```

3. Collect static files:
```bash
python manage.py collectstatic
```

## Langkah 6: Setup Web App

1. Buka Web tab di PythonAnywhere
2. Klik "Add a new web app"
3. Pilih "Manual configuration"
4. Pilih Python 3.11

### 6.1 Configure WSGI file
Edit file `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/myblog'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'myblog.settings'

# Serve Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 6.2 Configure Virtual Environment
Di Web tab, set:
- **Source code**: `/home/yourusername/myblog`
- **Working directory**: `/home/yourusername/myblog`
- **WSGI configuration file**: `/var/www/yourusername_pythonanywhere_com_wsgi.py`

## Langkah 7: Setup Static Files

1. Di Web tab, scroll ke "Static files"
2. Add static files:
   - URL: `/static/`
   - Directory: `/home/yourusername/myblog/staticfiles`

3. Add media files:
   - URL: `/media/`
   - Directory: `/home/yourusername/myblog/media`

## Langkah 8: Setup Environment Variables

1. Di Web tab, scroll ke "Environment variables"
2. Add:
   - `DEBUG`: `False`
   - `SECRET_KEY`: `your-secret-key`
   - `ALLOWED_HOSTS`: `yourusername.pythonanywhere.com`

## Langkah 9: Reload Web App

1. Klik "Reload" di Web tab
2. Tunggu beberapa menit
3. Akses website di: `https://yourusername.pythonanywhere.com`

## Langkah 10: Setup Google OAuth (Optional)

1. Update Google OAuth settings di Google Cloud Console
2. Tambahkan domain PythonAnywhere ke authorized domains
3. Update SocialApp di Django admin

## Troubleshooting

### Error 500
1. Cek error logs di Web tab
2. Pastikan semua dependencies terinstall
3. Cek file permissions

### Static files tidak muncul
1. Jalankan `python manage.py collectstatic`
2. Cek konfigurasi static files di Web tab
3. Reload web app

### Database error
1. Jalankan `python manage.py migrate`
2. Cek database permissions
3. Pastikan SQLite file ada

## Tips

1. **Gunakan Git** untuk version control
2. **Backup database** secara berkala
3. **Monitor error logs** di Web tab
4. **Test locally** sebelum deploy
5. **Gunakan environment variables** untuk sensitive data

## Upgrade ke Paid Plan (Optional)

Untuk fitur lebih:
- Custom domain
- HTTPS
- More storage
- Better performance
- Database MySQL/PostgreSQL

## Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
- Community Forum: https://www.pythonanywhere.com/forums/ 