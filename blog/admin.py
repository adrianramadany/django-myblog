from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Article, Gallery, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'article_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Jumlah Artikel'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'published_at', 'image_preview']
    list_filter = ['status', 'category', 'author', 'published_at', 'created_at']
    search_fields = ['title', 'content', 'author__username', 'category__name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-created_at']
    filter_horizontal = []
    raw_id_fields = ['author']
    readonly_fields = ['views', 'created_at', 'updated_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'image')
        }),
        ('Metadata', {
            'fields': ('category', 'author', 'status')
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'image_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_full_name', 'location', 'avatar_preview', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio']
    ordering = ['user__username']

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Nama Lengkap'

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', obj.avatar.url)
        return "No Avatar"
    avatar_preview.short_description = 'Avatar'

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'bio', 'avatar')
        }),
        ('Personal Details', {
            'fields': ('website', 'location', 'birth_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
