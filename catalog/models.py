from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    PUBLISH_STATUS = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    ]

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец',
                              null=True, blank=True, related_name='products')
    publish_status = models.CharField(max_length=20, choices=PUBLISH_STATUS,
                                      default='draft', verbose_name='Статус публикации')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name', 'price', 'created_at']
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_change_publish_status", "Может изменять статус публикации"),
        ]

    def __str__(self):
        return f"{self.name} ({self.price})"

    def save(self, *args, **kwargs):

        self.is_published = self.publish_status == 'published'
        super().save(*args, **kwargs)
