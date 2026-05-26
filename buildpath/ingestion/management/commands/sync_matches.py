from django.core.management.base import BaseCommand

from ingestion.pipeline.seed import run_seed

VALID_PLATFORMS = ["na1", "euw1", "eun1", "kr", "jp1", "br1", "la1", "la2", "oc1", "tr1", "ru"]
VALID_TIERS = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND"]
VALID_DIVISIONS = ["I", "II", "III", "IV"]


class Command(BaseCommand):
    help = "Seed match data from Riot API using BFS match-graph crawling"

    def add_arguments(self, parser):
        parser.add_argument("--region", required=True, choices=VALID_PLATFORMS)
        parser.add_argument("--tier", required=True, choices=VALID_TIERS)
        parser.add_argument("--division", required=True, choices=VALID_DIVISIONS)
        parser.add_argument("--max-players", type=int, default=None)

    def handle(self, *args, **kwargs):
        platform = kwargs["region"]
        tier = kwargs["tier"].upper()
        division = kwargs["division"].upper()
        max_players = kwargs["max_players"]

        self.stdout.write(f"Starting match ingestion: {platform} / {tier} {division}")
        run_seed(platform, tier, division, max_players=max_players)
        self.stdout.write(self.style.SUCCESS("Done."))
