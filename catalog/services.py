from django.core.cache import cache
from .models import Product, Category


def get_all_products():
    """
    Сервисная функция для получения всех опубликованных продуктов
    с низкоуровневым кешированием
    """
    cache_key = 'all_published_products'
    cached_products = cache.get(cache_key)

    if cached_products is not None:
        return cached_products

    products = Product.objects.filter(
        is_published=True
    ).select_related('category')

    cache.set(cache_key, products, timeout=300)
    return products


def get_products_by_category(category_slug=None):
    """
    Сервисная функция для получения всех продуктов в указанной категории
    с низкоуровневым кешированием
    """
    cache_key = f'products_category_{category_slug if category_slug else "all"}'
    cached_products = cache.get(cache_key)

    if cached_products is not None:
        return cached_products

    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(
                category=category,
                is_published=True
            ).select_related('category')
        except Category.DoesNotExist:
            products = get_all_products()
    else:
        products = get_all_products()

    cache.set(cache_key, products, timeout=300)
    return products


def get_categories_with_products():
    """
    Возвращает все категории с количеством продуктов в каждой
    с низкоуровневым кешированием
    """
    cache_key = 'categories_with_products'
    cached_categories = cache.get(cache_key)

    if cached_categories is not None:
        return cached_categories

    categories = Category.objects.all()
    categories_with_count = []

    for category in categories:
        product_count = Product.objects.filter(
            category=category,
            is_published=True
        ).count()
        categories_with_count.append({
            'category': category,
            'product_count': product_count
        })

    cache.set(cache_key, categories_with_count, timeout=600)
    return categories_with_count