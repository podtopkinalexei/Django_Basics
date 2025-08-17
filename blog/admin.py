from django.contrib import admin
from django.contrib.admin import AdminSite
from blog.models import BlogPost

class BlogAdminSite(AdminSite):
    site_header = "Управление блогом"
    site_title = "Админка блога"
    index_title = "Управление контентом блога"

blog_admin_site = BlogAdminSite(name='blogadmin')

@admin.register(BlogPost, site=blog_admin_site)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'views_count')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')


admin.site.site_header = "Панель администрирования"