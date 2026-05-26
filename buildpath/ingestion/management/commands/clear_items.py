from django.core.management.base import BaseCommand

from items.models import Item


class Command(BaseCommand):
    help = "Delete all Item records"

    def handle(self, *args, **kwargs):
        count, _ = Item.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} items."))
