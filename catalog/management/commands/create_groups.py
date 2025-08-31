from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группы с соответствующими правами'

    def handle(self, *args, **options):

        content_type = ContentType.objects.get_for_model(Product)

        can_unpublish = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type
        )
        can_change_status = Permission.objects.get(
            codename='can_change_publish_status',
            content_type=content_type
        )
        delete_permission = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )
        change_permission = Permission.objects.get(
            codename='change_product',
            content_type=content_type
        )

        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        moderator_group.permissions.add(
            can_unpublish,
            can_change_status,
            delete_permission,
            change_permission
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Модератор продуктов" создана с правами')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Модератор продуктов" уже существует')
            )
