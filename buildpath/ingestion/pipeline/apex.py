from django.utils import timezone

from ingestion.clients.league import get_apex_league
from ingestion.clients.match import get_match, get_match_ids
from ingestion.pipeline.seed import PLATFORM_TO_REGION
from ingestion.services.matches import ingest_match
from matches.models import Match, Player


def run_apex(platform, tier, max_players=None):
    region = PLATFORM_TO_REGION[platform.lower()]
    rank = tier.upper()

    print(f"[apex] Fetching {tier} player list...")
    entries = get_apex_league(platform, tier)
    if max_players:
        entries = entries[:max_players]
    total = len(entries)
    print(f"[apex] {total} players found")

    for i, entry in enumerate(entries, start=1):
        puuid = entry["puuid"]
        now = timezone.now()

        Player.objects.update_or_create(
            puuid=puuid,
            defaults={"platform": platform}
        )

        match_ids = get_match_ids(region, puuid)
        existing = set(Match.objects.filter(match_id__in=match_ids).values_list("match_id", flat=True))
        print(f"[apex] [{i}/{total}] {puuid[:16]}...: {len(match_ids)} matches found ({len(existing)} already ingested)")

        for match_id in match_ids:
            if match_id in existing:
                continue
            try:
                print(f"[apex]   Ingesting {match_id}...")
                match_data = get_match(region, match_id)
                ingest_match(match_data, platform, rank=rank)
            except Exception as e:
                print(f"[apex]   ERROR ingesting {match_id}: {e}")

        Player.objects.filter(puuid=puuid).update(last_checked=now)
