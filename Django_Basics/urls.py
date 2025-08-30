from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog.admin import blog_admin_site

urlpatterns = [
    path('admin/blog/', blog_admin_site.urls),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('', include('catalog.urls', namespace='catalog')),
    path('blog/', include('blog.urls', namespace='blog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)