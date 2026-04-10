from django.core.management.base import BaseCommand
from ingestion.services.items import sync_items

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sync_items()