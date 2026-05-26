from django.core.management.base import BaseCommand
from django.db.models import Count

from matches.models import Match

TIER_ORDER = [
    "IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM",
    "EMERALD", "DIAMOND", "MASTER", "GRANDMASTER", "CHALLENGER",
]


class Command(BaseCommand):
    help = "Show number of tracked matches per tier"

    def handle(self, *args, **kwargs):
        counts = {
            row["rank"]: row["count"]
            for row in Match.objects.values("rank").annotate(count=Count("id"))
        }

        total = 0
        for tier in TIER_ORDER:
            count = counts.get(tier, 0)
            if count == 0:
                continue
            self.stdout.write(f"  {tier:<20} {count}")
            total += count

        unranked = counts.get(None, 0)
        if unranked:
            self.stdout.write(f"  {'Unranked':<20} {unranked}")
            total += unranked

        self.stdout.write(self.style.SUCCESS(f"\n  Total: {total}"))
