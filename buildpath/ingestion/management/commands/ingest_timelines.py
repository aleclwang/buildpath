from django.core.management.base import BaseCommand
from matches.models import Match
from ingestion.pipeline.seed import PLATFORM_TO_REGION
from ingestion.services.timelines import ingest_timeline


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=None)

    def handle(self, *args, **kwargs):
        qs = (
            Match.objects.exclude(platform__isnull=True)
            .filter(participant__build_order=[])
            .distinct()
            .values_list("match_id", "platform")
        )
        if kwargs["limit"]:
            qs = qs[: kwargs["limit"]]
        matches = list(qs)
        total = len(matches)
        print(f"[timelines] {total} matches to process")

        for i, (match_id, platform) in enumerate(matches, start=1):
            region = PLATFORM_TO_REGION.get(platform.lower())
            if not region:
                print(f"[timelines] [{i}/{total}] Skipping {match_id}: unknown platform {platform}")
                continue
            try:
                ingest_timeline(match_id, region)
                print(f"[timelines] [{i}/{total}] {match_id} OK")
            except Exception as e:
                print(f"[timelines] [{i}/{total}] {match_id} ERROR: {e}")
