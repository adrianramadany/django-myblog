from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from blog.models import Category, Article, Gallery, UserProfile
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create groups
        admin_group, created = Group.objects.get_or_create(name='Admin')
        author_group, created = Group.objects.get_or_create(name='Author')
        
        if created:
            self.stdout.write('Created groups: Admin, Author')

        # Create sample users
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            admin_user.groups.add(admin_group)
            admin_user.is_staff = True
            admin_user.save()
            UserProfile.objects.create(user=admin_user)
            self.stdout.write('Created admin user')

        if not User.objects.filter(username='author1').exists():
            author1 = User.objects.create_user(
                username='author1',
                email='author1@example.com',
                password='author123',
                first_name='John',
                last_name='Doe'
            )
            author1.groups.add(author_group)
            author1.save()
            UserProfile.objects.create(
                user=author1,
                bio='Web developer and tech enthusiast',
                location='Jakarta, Indonesia',
                website='https://johndoe.com'
            )
            self.stdout.write('Created author1 user')

        if not User.objects.filter(username='author2').exists():
            author2 = User.objects.create_user(
                username='author2',
                email='author2@example.com',
                password='author123',
                first_name='Jane',
                last_name='Smith'
            )
            author2.groups.add(author_group)
            author2.save()
            UserProfile.objects.create(
                user=author2,
                bio='Content writer and blogger',
                location='Bandung, Indonesia',
                website='https://janesmith.com'
            )
            self.stdout.write('Created author2 user')

        # Create categories
        categories_data = [
            {'name': 'Technology', 'description': 'Artikel tentang teknologi terbaru'},
            {'name': 'Programming', 'description': 'Tutorial dan tips programming'},
            {'name': 'Web Development', 'description': 'Pembahasan seputar web development'},
            {'name': 'Design', 'description': 'Artikel tentang design dan UI/UX'},
            {'name': 'Business', 'description': 'Artikel seputar bisnis dan entrepreneurship'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample articles
        articles_data = [
            {
                'title': 'Memulai dengan Django Framework',
                'content': '''
                Django adalah framework web Python yang powerful dan mudah digunakan. Framework ini mengikuti pola MVT (Model-View-Template) dan menyediakan banyak fitur built-in yang memudahkan pengembangan web.

                ## Keunggulan Django:
                - **Admin Interface**: Django menyediakan admin interface yang otomatis
                - **ORM**: Object-Relational Mapping yang powerful
                - **Security**: Fitur keamanan built-in
                - **Scalability**: Mudah di-scale untuk aplikasi besar

                ## Cara Memulai:
                1. Install Python dan pip
                2. Install Django: `pip install django`
                3. Buat project: `django-admin startproject myproject`
                4. Jalankan server: `python manage.py runserver`

                Django sangat cocok untuk pengembangan web yang cepat dan aman.
                ''',
                'category': 'Programming',
                'author': 'author1',
                'status': 'published'
            },
            {
                'title': 'Tips Optimasi Website',
                'content': '''
                Optimasi website sangat penting untuk meningkatkan performa dan user experience. Berikut adalah beberapa tips yang bisa diterapkan:

                ## Optimasi Gambar:
                - Gunakan format yang tepat (WebP, JPEG, PNG)
                - Compress gambar tanpa mengurangi kualitas
                - Gunakan lazy loading

                ## Optimasi CSS dan JavaScript:
                - Minify file CSS dan JS
                - Gunakan CDN untuk library eksternal
                - Implementasikan caching

                ## Optimasi Database:
                - Gunakan indexing yang tepat
                - Optimasi query database
                - Implementasikan caching

                Dengan optimasi yang tepat, website akan lebih cepat dan user-friendly.
                ''',
                'category': 'Web Development',
                'author': 'author2',
                'status': 'published'
            },
            {
                'title': 'Trend Teknologi 2024',
                'content': '''
                Tahun 2024 membawa berbagai trend teknologi yang menarik. Mari kita bahas beberapa trend yang sedang berkembang:

                ## Artificial Intelligence:
                AI semakin berkembang dengan munculnya berbagai model seperti GPT-4, Claude, dan lainnya. AI digunakan dalam berbagai bidang seperti healthcare, finance, dan education.

                ## Web3 dan Blockchain:
                Teknologi blockchain terus berkembang dengan munculnya berbagai aplikasi DeFi dan NFT yang inovatif.

                ## Edge Computing:
                Edge computing memungkinkan pemrosesan data lebih dekat dengan sumber data, mengurangi latency dan meningkatkan efisiensi.

                ## Sustainability Tech:
                Teknologi ramah lingkungan semakin mendapat perhatian dengan fokus pada renewable energy dan green computing.

                Trend teknologi ini akan terus berkembang dan mempengaruhi berbagai aspek kehidupan kita.
                ''',
                'category': 'Technology',
                'author': 'author1',
                'status': 'published'
            },
            {
                'title': 'Prinsip Design yang Baik',
                'content': '''
                Design yang baik tidak hanya tentang estetika, tetapi juga tentang fungsionalitas dan user experience. Berikut adalah beberapa prinsip design yang penting:

                ## Hierarchy:
                Gunakan hierarchy visual untuk memandu user melalui konten dengan urutan yang logis.

                ## Consistency:
                Konsistensi dalam design membantu user memahami interface dengan lebih mudah.

                ## Accessibility:
                Design harus dapat diakses oleh semua user, termasuk yang memiliki keterbatasan.

                ## Simplicity:
                Design yang sederhana dan clean lebih efektif daripada design yang kompleks.

                ## Feedback:
                Berikan feedback yang jelas kepada user untuk setiap interaksi.

                Dengan menerapkan prinsip-prinsip ini, design akan lebih efektif dan user-friendly.
                ''',
                'category': 'Design',
                'author': 'author2',
                'status': 'published'
            },
            {
                'title': 'Strategi Marketing Digital',
                'content': '''
                Marketing digital menjadi sangat penting di era digital seperti sekarang. Berikut adalah beberapa strategi yang efektif:

                ## Content Marketing:
                Buat konten yang berkualitas dan relevan untuk target audience Anda.

                ## Social Media Marketing:
                Manfaatkan platform social media untuk menjangkau audience yang lebih luas.

                ## SEO:
                Optimasi search engine untuk meningkatkan visibility website.

                ## Email Marketing:
                Email marketing masih menjadi salah satu channel marketing yang efektif.

                ## Influencer Marketing:
                Kolaborasi dengan influencer untuk menjangkau audience yang lebih spesifik.

                Kombinasi berbagai strategi ini akan memberikan hasil yang optimal untuk bisnis Anda.
                ''',
                'category': 'Business',
                'author': 'author1',
                'status': 'published'
            }
        ]

        for article_data in articles_data:
            category = Category.objects.get(name=article_data['category'])
            author = User.objects.get(username=article_data['author'])
            
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'content': article_data['content'],
                    'category': category,
                    'author': author,
                    'status': article_data['status'],
                    'published_at': timezone.now() - timedelta(days=len(articles_data) - articles_data.index(article_data))
                }
            )
            if created:
                self.stdout.write(f'Created article: {article.title}')

        # Create sample gallery items
        gallery_data = [
            {
                'title': 'Workspace Setup',
                'description': 'Setup workspace yang nyaman untuk produktivitas maksimal'
            },
            {
                'title': 'Coding Session',
                'description': 'Sesi coding yang produktif dengan tools terbaik'
            },
            {
                'title': 'Team Meeting',
                'description': 'Meeting tim untuk brainstorming ide-ide kreatif'
            }
        ]

        for gallery_item in gallery_data:
            gallery, created = Gallery.objects.get_or_create(
                title=gallery_item['title'],
                defaults={'description': gallery_item['description']}
            )
            if created:
                self.stdout.write(f'Created gallery item: {gallery.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        ) 