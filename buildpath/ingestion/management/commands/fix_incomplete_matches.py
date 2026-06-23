from django.core.management.base import BaseCommand
from django.db.models import Count

from ingestion.clients.match import get_match
from ingestion.pipeline.seed import PLATFORM_TO_REGION
from ingestion.services.matches import ingest_match
from matches.models import Match


class Command(BaseCommand):
    help = "Re-ingest matches that have fewer than 10 participants"

    def add_arguments(self, parser):
        parser.add_argument("--min-participants", type=int, default=10)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **kwargs):
        min_participants = kwargs["min_participants"]
        dry_run = kwargs["dry_run"]

        incomplete = (
            Match.objects.annotate(p_count=Count("participant"))
            .filter(p_count__lt=min_participants)
        )
        total = incomplete.count()
        self.stdout.write(f"Found {total} matches with fewer than {min_participants} participants")

        if dry_run:
            for match in incomplete:
                self.stdout.write(f"  {match.match_id} (platform={match.platform}, participants={match.p_count})")
            return

        fixed = 0
        failed = 0
        for match in incomplete:
            platform = match.platform
            if not platform:
                self.stdout.write(self.style.WARNING(f"  Skipping {match.match_id}: no platform recorded"))
                failed += 1
                continue
            region = PLATFORM_TO_REGION.get(platform.lower())
            if not region:
                self.stdout.write(self.style.WARNING(f"  Skipping {match.match_id}: unknown platform {platform}"))
                failed += 1
                continue
            try:
                self.stdout.write(f"  Re-ingesting {match.match_id}...")
                match_data = get_match(region, match.match_id)
                ingest_match(match_data, platform, rank=match.rank)
                fixed += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ERROR on {match.match_id}: {e}"))
                failed += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Fixed: {fixed}, Failed/skipped: {failed}"))
