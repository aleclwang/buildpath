from django.core.management.base import BaseCommand
from ingestion.services.champions import sync_champions


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sync_champions()
