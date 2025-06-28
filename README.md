# MyBlog - Platform Blog Profesional

MyBlog adalah platform blog profesional yang dibangun dengan Django untuk tugas UAS Web Lanjut. Platform ini menawarkan fitur lengkap untuk manajemen konten blog dengan antarmuka yang modern dan responsif.

## 🚀 Fitur Utama

### 1. Landing Page
- Hero section yang menarik dengan Material Kit design
- Daftar artikel terbaru dan unggulan
- Navigasi ke halaman About, Login/Register, dan Dashboard
- Responsive design untuk semua perangkat

### 2. Authentication System
- Halaman Login dan Register yang user-friendly
- Sistem autentikasi Django yang aman
- Role-based access control (Admin, Author)
- User profile management

### 3. Dashboard Admin/Author
- Dashboard dengan statistik real-time
- Grafik Chart.js untuk visualisasi data
- Menu navigasi lengkap: Artikel, Kategori, Galeri, Users
- Notifikasi/alert untuk setiap aksi CRUD

### 4. CRUD Operations
- **Artikel**: Create, Read, Update, Delete dengan gambar dan kategori
- **Kategori**: Manajemen kategori artikel
- **Galeri**: Upload dan manajemen gambar
- **User Management**: Edit role dan group user

### 5. Public Features
- Daftar artikel dengan search dan filter
- Detail artikel dengan social sharing
- Halaman About/CV yang profesional
- Pagination untuk performa optimal

## 🛠️ Teknologi yang Digunakan

- **Backend**: Django 5.2.3
- **Frontend**: Bootstrap 5, Material Kit Design
- **Database**: SQLite (development), PostgreSQL (production)
- **Image Processing**: Pillow
- **Charts**: Chart.js
- **Icons**: Font Awesome 6

## 📋 Prerequisites

Sebelum menjalankan project, pastikan Anda memiliki:

- Python 3.8 atau lebih baru
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd myblog
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Akses aplikasi di: http://127.0.0.1:8000/

## 📁 Struktur Project

```
myblog/
├── blog/                    # Main app
│   ├── migrations/         # Database migrations
│   ├── templates/blog/     # Blog templates
│   ├── admin.py           # Admin configuration
│   ├── forms.py           # Django forms
│   ├── models.py          # Database models
│   ├── urls.py            # URL patterns
│   └── views.py           # View functions
├── myblog/                # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/             # Base templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🗄️ Database Models

### Article
- Title, content, excerpt
- Image upload
- Category relationship
- Author relationship
- Status (draft/published)
- View counter
- Timestamps

### Category
- Name, description
- Slug for SEO
- Article count

### Gallery
- Title, description
- Image upload
- Timestamps

### UserProfile
- Bio, avatar
- Website, location
- Birth date
- User relationship

## 🔐 User Roles & Permissions

### Admin
- Akses penuh ke semua fitur
- User management
- Dashboard dengan statistik lengkap

### Author
- Create, edit, delete artikel sendiri
- Upload gambar ke galeri
- Akses dashboard terbatas

### Public User
- Baca artikel
- Register/Login
- View halaman About

## 🎨 UI/UX Features

- **Material Kit Design**: Modern dan profesional
- **Responsive**: Optimal di desktop, tablet, mobile
- **Dark/Light Theme**: Konsisten dengan Material Design
- **Interactive Elements**: Hover effects, animations
- **Accessibility**: Semantic HTML, ARIA labels

## 📊 Dashboard Features

- **Statistics Cards**: Total artikel, kategori, users
- **Charts**: Artikel per kategori (Chart.js)
- **Recent Articles**: Daftar artikel terbaru
- **Quick Actions**: Create, edit, delete
- **User Stats**: Top authors

## 🔍 Search & Filter

- **Search Articles**: By title, content, author
- **Category Filter**: Filter by category
- **Pagination**: Efficient data loading
- **Sorting**: By date, views, title

## 📱 Social Features

- **Social Sharing**: Facebook, Twitter, LinkedIn, WhatsApp
- **Related Articles**: Artikel terkait
- **Author Info**: Profile penulis
- **Newsletter Signup**: Email subscription

## 🚀 Deployment

### PythonAnywhere Setup

1. **Upload Files**
   - Upload semua file ke PythonAnywhere
   - Pastikan struktur folder benar

2. **Setup Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 myblog
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

5. **Configure WSGI**
   - Edit WSGI file sesuai path project
   - Set environment variables

6. **Configure Settings**
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Set `SECRET_KEY`

## 🐛 Troubleshooting

### Common Issues

1. **ImportError: No module named 'django'**
   - Pastikan virtual environment aktif
   - Install dependencies: `pip install -r requirements.txt`

2. **Database errors**
   - Run migrations: `python manage.py migrate`
   - Check database settings

3. **Static files not loading**
   - Run: `python manage.py collectstatic`
   - Check `STATIC_URL` and `STATIC_ROOT` settings

4. **Media files not uploading**
   - Check `MEDIA_URL` and `MEDIA_ROOT` settings
   - Ensure directory permissions

## 📝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is created for educational purposes as part of Web Lanjut course assignment.

## 👨‍💻 Author

**Adrian Ramadany**
- Email: adrianramadany739@gmail.com
- Course: Web Lanjut
- Semester: UAS Project

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Material Kit Design
- Font Awesome
- Chart.js

---

**MyBlog** - Professional Blog Platform for UAS Web Lanjut 