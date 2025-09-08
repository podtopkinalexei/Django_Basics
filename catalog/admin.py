from django.contrib import admin
from django.utils.html import format_html
from catalog.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')
    list_display_links = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'image_preview', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    list_editable = ('price', 'category')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_display_links = ('id', 'name')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description')
        }),
        ('Изображение и категория', {
            'fields': ('image', 'image_preview', 'category'),
            'description': 'Загрузите новое изображение или измените категорию'
        }),
        ('Финансы и даты', {
            'fields': ('price', ('created_at', 'updated_at')),
            'classes': ('collapse',)  # Сворачиваемый блок
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border: 1px solid #ddd; border-radius: 4px; padding: 5px;"/>',
                obj.image.url
            )
        return format_html('<span style="color: #999;">Нет изображения</span>')

    image_preview.short_description = 'Текущее изображение'
    image_preview.allow_tags = True