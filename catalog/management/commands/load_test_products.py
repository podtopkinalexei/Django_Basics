from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загружает тестовые продукты в базу данных (удаляя старые данные)'

    def handle(self, *args, **options):
        # Удаляем старые данные
        self.stdout.write("Удаление старых данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем категории
        categories = [
            Category(name="Смартфоны", description="Мобильные телефоны"),
            Category(name="Планшеты", description="Портативные компьютеры"),
            Category(name="Аксессуары", description="Чехлы и другие аксессуары")
        ]
        Category.objects.bulk_create(categories)
        self.stdout.write("Создано 3 категории")

        # Получаем созданные категории
        smartphones = Category.objects.get(name="Смартфоны")
        tablets = Category.objects.get(name="Планшеты")
        accessories = Category.objects.get(name="Аксессуары")

        # Создаем продукты
        products = [
            Product(
                name="iPhone 15 Pro",
                description="Флагман Apple",
                category=smartphones,
                price=99990.00,
                created_at=timezone.now(),
                updated_at=timezone.now()
            ),
            Product(
                name="Samsung Galaxy S23",
                description="Флагман Samsung",
                category=smartphones,
                price=89990.00,
                created_at=timezone.now(),
                updated_at=timezone.now()
            ),
            Product(
                name="iPad Pro",
                description="Планшет Apple",
                category=tablets,
                price=74990.00,
                created_at=timezone.now(),
                updated_at=timezone.now()
            ),
            Product(
                name="Чехол для iPhone",
                description="Силиконовый чехол",
                category=accessories,
                price=1990.00,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
        ]
        Product.objects.bulk_create(products)

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создано {Category.objects.count()} категорий и "
                f"{Product.objects.count()} продуктов"
            )
        )
