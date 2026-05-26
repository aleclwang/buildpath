from django.core.management.base import BaseCommand
from django.db.models import Count

from matches.models import Player


class Command(BaseCommand):
    help = "Show number of tracked players per platform"

    def handle(self, *args, **kwargs):
        counts = {
            row["platform"]: row["count"]
            for row in Player.objects.values("platform").annotate(count=Count("puuid"))
        }

        total = 0
        for platform, count in sorted(counts.items()):
            self.stdout.write(f"  {platform:<10} {count}")
            total += count

        self.stdout.write(self.style.SUCCESS(f"\n  Total: {total}"))
