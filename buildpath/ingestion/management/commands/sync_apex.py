from django.core.management.base import BaseCommand

from ingestion.pipeline.apex import run_apex

VALID_PLATFORMS = ["na1", "euw1", "eun1", "kr", "jp1", "br1", "la1", "la2", "oc1", "tr1", "ru"]
VALID_TIERS = ["MASTER", "GRANDMASTER", "CHALLENGER"]


class Command(BaseCommand):
    help = "Ingest match data for all players in an apex tier (Master, Grandmaster, Challenger)"

    def add_arguments(self, parser):
        parser.add_argument("--region", required=True, choices=VALID_PLATFORMS)
        parser.add_argument("--tier", required=True, choices=VALID_TIERS)
        parser.add_argument("--max-players", type=int, default=None)

    def handle(self, *args, **kwargs):
        platform = kwargs["region"]
        tier = kwargs["tier"].upper()
        max_players = kwargs["max_players"]

        self.stdout.write(f"Starting apex ingestion: {platform} / {tier}")
        run_apex(platform, tier, max_players=max_players)
        self.stdout.write(self.style.SUCCESS("Done."))
